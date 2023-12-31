"""
ASGI config for UserManagement project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# from django.urls import path

# from channels.routing import ProtocolTypeRouter, URLRouter

# from channels.auth import AuthMiddlewareStack

# from chat.consumers import PersonalChatConsumer

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserManagement.settings')

# # application = get_asgi_application()


# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter([
#             path('ws/<int:id>/', PersonalChatConsumer),
#         ])
#     )
# })

import os

from django.core.asgi import get_asgi_application

from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter

from channels.auth import AuthMiddlewareStack

from chat.consumers import PersonalChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UserManagement.settings')

django_asgi = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi,
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
        ])
    )
})
