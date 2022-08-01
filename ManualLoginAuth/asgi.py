"""
ASGI config for ManualLoginAuth project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import socketio
from django.core.asgi import get_asgi_application
from socketio_server.views import sio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ManualLoginAuth.settings')

django_app = get_asgi_application()
application = socketio.ASGIApp(sio, django_app)
