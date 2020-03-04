import time
import edgeiq
import argparse
import socketio
import cv2
import base64
"""
Use object detection to detect objects in the frame in realtime. The
types of objects detected can be changed by selecting different models.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

sio = socketio.Client(logger=True, engineio_logger=True)


@sio.event
def connect():
    print('[INFO] Successfully connected to server.')


@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')


@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')


class CVClient(object):
    def __init__(self, server_addr):
        self.server_addr = server_addr
        self.server_port = 5001

    def setup(self):
        print('[INFO] Connecting to server http://{}:{}...'.format(
            self.server_addr, self.server_port))
        sio.connect(
                'http://{}:{}'.format(self.server_addr, self.server_port),
                transports=['websocket'],
                namespaces=['/cv'])
        time.sleep(1)
        return self

    def _convert_image_to_jpeg(self, image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame, text):
        frame = edgeiq.resize(
                frame, width=640, height=480, keep_scale=True)
        sio.emit(
                'cv2server',
                {
                    'image': self._convert_image_to_jpeg(frame),
                    'text': '<br />'.join(text)
                })

    def check_exit(self):
        pass

    def close(self):
        sio.disconnect()


def main(camera, use_streamer, server_addr):
    obj_detect = edgeiq.ObjectDetection(
            "alwaysai/mobilenet_ssd")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()

    try:
        streamer = None
        if use_streamer:
            streamer = edgeiq.Streamer().setup()
        else:
            streamer = CVClient(server_addr).setup()

        with edgeiq.WebcamVideoStream(cam=camera) as video_stream:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # loop detection
            while True:
                frame = video_stream.read()
                results = obj_detect.detect_objects(frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                        frame, results.predictions, colors=obj_detect.colors)

                # Generate text to display on streamer
                text = ["Model: {}".format(obj_detect.model_id)]
                text.append(
                        "Inference time: {:1.3f} s".format(results.duration))
                text.append("Objects:")

                for prediction in results.predictions:
                    text.append("{}: {:2.2f}%".format(
                        prediction.label, prediction.confidence * 100))

                streamer.send_data(frame, text)

                fps.update()

                if streamer.check_exit():
                    break

    finally:
        if streamer is not None:
            streamer.close()
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Realtime Object Detector')
    parser.add_argument(
            '--camera', type=int, default='0',
            help='The camera index to stream from.')
    parser.add_argument(
            '--use-streamer',  action='store_true',
            help='Use the streamer instead of connecting to the server.')
    parser.add_argument(
            '--server-addr',  type=str, default='localhost',
            help='The IP address or hostname of the SocketIO server.')
    args = parser.parse_args()
    main(args.camera, args.use_streamer, args.server_addr)
