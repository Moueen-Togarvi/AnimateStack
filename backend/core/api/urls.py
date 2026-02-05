from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, CategoryViewSet, TagViewSet, AssetViewSet
from marketplace.views import LikeViewSet, CommentViewSet, CollectionViewSet

router = DefaultRouter()
router.register(r'components', ComponentViewSet, basename='component')
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'collections', CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
]
