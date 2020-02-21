from flask_socketio import SocketIO
from flask import Flask, render_template

app = Flask(__name__)
socketio = SocketIO(app)

@_app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

if __name == "__main__":
    socketio.run(app=app)
