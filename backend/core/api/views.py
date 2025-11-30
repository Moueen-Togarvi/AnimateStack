from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Component, Category, Tag, Asset
from .serializers import ComponentSerializer, CategorySerializer, TagSerializer, AssetSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class ComponentViewSet(viewsets.ModelViewSet):
    serializer_class = ComponentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'tags__name']
    ordering_fields = ['created_at', 'views', 'downloads']
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Component.objects.all()
        creator_id = self.request.query_params.get('creator', None)
        if creator_id:
            queryset = queryset.filter(creator__id=creator_id)
        else:
            queryset = queryset.filter(is_public=True)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, slug=None):
        component = self.get_object()
        if component.likes.filter(id=request.user.id).exists():
            component.likes.remove(request.user)
            return Response({'status': 'unliked'})
        else:
            component.likes.add(request.user)
            return Response({'status': 'liked'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def view(self, request, slug=None):
        component = self.get_object()
        component.views += 1
        component.save()
        return Response({'status': 'viewed'})

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
