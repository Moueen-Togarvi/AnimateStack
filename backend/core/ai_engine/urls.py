from django.urls import path
from .views import GenerateComponentView

urlpatterns = [
    path('generate/', GenerateComponentView.as_view(), name='generate-component'),
]
