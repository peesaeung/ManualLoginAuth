from django.apps import AppConfig
import socketio


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'socketio_server'


sio = socketio.Server()
app = socketio.ASGIApp(sio)


@sio.event
async def my_event(sid, data):
    pass


@sio.on('*')    # on
async def catch_all(event, sid, data):
    pass
