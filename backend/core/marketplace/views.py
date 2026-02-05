from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Like, Comment, Collection
from .serializers import LikeSerializer, CommentSerializer, CollectionSerializer

class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Like.objects.all()

    def perform_create(self, serializer):
        # Check if already liked
        user = self.request.user
        component = serializer.validated_data['component']
        if Like.objects.filter(user=user, component=component).exists():
            raise serializers.ValidationError("You have already liked this component.")
        serializer.save(user=user)

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle_like(self, request):
        component_id = request.data.get('component_id')
        if not component_id:
            return Response({'error': 'component_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        try:
            like = Like.objects.get(user=user, component_id=component_id)
            like.delete()
            return Response({'status': 'unliked'})
        except Like.DoesNotExist:
            Like.objects.create(user=user, component_id=component_id)
            return Response({'status': 'liked'})

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')
        component_id = self.request.query_params.get('component_id')
        if component_id:
            queryset = queryset.filter(component_id=component_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Collection.objects.filter(user=user) | Collection.objects.filter(is_public=True)
        return Collection.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
