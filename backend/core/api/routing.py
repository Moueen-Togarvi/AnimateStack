from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/components/(?P<slug>[\w-]+)/$', consumers.ComponentConsumer.as_asgi()),
]
