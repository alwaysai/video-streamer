from flask_socketio import SocketIO
from flask import Flask, render_template

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')

if __name__ == "__main__":
    socketio.run(app=app)
