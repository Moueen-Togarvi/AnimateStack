from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, CategoryViewSet, TagViewSet, AssetViewSet

router = DefaultRouter()
router.register(r'components', ComponentViewSet, basename='component')
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'assets', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
