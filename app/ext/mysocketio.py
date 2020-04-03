from flask_socketio import SocketIO
import time

# from app.lib import get_running_state_sql

socketio = SocketIO()


#@socketio.on('event_start', namespace='/test')
#def event_start():
#    print('receive event_start')
#    time.sleep(2)
#    while True:
#        if get_running_state_sql():
#            print('wait')
#            socketio.sleep(2)
#        else:
#            print('socketio emit event_done')
#            socketio.emit('event_done', namespace='/test', broadcast=True)
#            # break
#            return 0
#
