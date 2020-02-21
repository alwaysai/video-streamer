from flask_socketio import SocketIO
from flask import Flask, render_template, request

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('[INFO] Client connected: {}'.format(request.sid))

@socketio.on('disconnect')
def disconnect():
    print('[INFO] Client disconnected: {}'.format(request.sid))

if __name__ == "__main__":
    socketio.run(app=app)
