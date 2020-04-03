from flask_socketio import SocketIO

socketio = SocketIO()

def init_ext(app):
    socketio.init_app(app)
