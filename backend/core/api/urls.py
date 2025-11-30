from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'components', ComponentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
