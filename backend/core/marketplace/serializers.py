from rest_framework import serializers
from .models import Like, Comment, Collection
from users.serializers import UserSerializer

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'user', 'component', 'created_at')
        read_only_fields = ('user', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'user', 'component', 'text', 'created_at')
        read_only_fields = ('user', 'created_at')

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'user', 'name', 'description', 'components', 'is_public', 'created_at')
        read_only_fields = ('user', 'created_at')
