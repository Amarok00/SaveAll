"""
ASGI config for Save_all project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os


from django.core.asgi import get_asgi_application  # noqa

from channels.routing import ProtocolTypeRouter, URLRouter  # noqa
from channels.auth import AuthMiddlewareStack  # noqa
import chats.routing  # noqa
import notifications.routing  # noqa

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Save_all.settings")
django_asgi_app = get_asgi_application()  # noqa


# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chats.routing.websocket_urlpatterns
                + notifications.routing.websocket_urlpatterns
            )
        ),
    }
)
