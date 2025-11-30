from rest_framework import serializers
from .models import Component, Category, Tag
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ComponentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', write_only=True, many=True, required=False
    )
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Component
        fields = (
            'id', 'title', 'slug', 'description', 'code_content', 
            'preview_url', 'price', 'is_public', 'created_at', 
            'creator', 'category', 'category_id', 'tags', 'tag_ids',
            'views', 'downloads', 'likes_count', 'is_liked'
        )
        read_only_fields = ('views', 'downloads', 'slug')

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        component = Component.objects.create(**validated_data)
        component.tags.set(tags)
        return component
