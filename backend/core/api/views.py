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
        user = self.request.user
        
        # Admin sees all
        if user.is_staff:
            return queryset
            
        # Creator sees their own (even unapproved)
        if user.is_authenticated:
            queryset = queryset.filter(Q(is_approved=True) | Q(creator=user))
        else:
            queryset = queryset.filter(is_approved=True, is_public=True)
            
        creator_id = self.request.query_params.get('creator', None)
        if creator_id:
            queryset = queryset.filter(creator__id=creator_id)
            
        return queryset

    def perform_create(self, serializer):
        import json
        import os
        from django.utils.text import slugify
        
        # Auto-categorization Logic
        data = self.request.data
        title = data.get('title', '').lower()
        description = data.get('description', '').lower()
        combined_text = f"{title} {description}"
        
        category = None
        
        # Simple keyword matching
        if 'button' in combined_text:
            category, _ = Category.objects.get_or_create(name='Buttons', defaults={'slug': 'buttons', 'icon': '🔘'})
        elif 'card' in combined_text:
            category, _ = Category.objects.get_or_create(name='Cards', defaults={'slug': 'cards', 'icon': '🃏'})
        elif 'loader' in combined_text or 'spinner' in combined_text or 'loading' in combined_text:
            category, _ = Category.objects.get_or_create(name='Loaders', defaults={'slug': 'loaders', 'icon': '⏳'})
        elif 'input' in combined_text or 'form' in combined_text:
            category, _ = Category.objects.get_or_create(name='Inputs', defaults={'slug': 'inputs', 'icon': '⌨️'})
        elif 'nav' in combined_text or 'menu' in combined_text:
            category, _ = Category.objects.get_or_create(name='Navigation', defaults={'slug': 'navigation', 'icon': '🧭'})
            
        # Save to DB first
        component = serializer.save(creator=self.request.user, category=category)
        
        # Save to Local Disk
        local_dir = "y:/worksapace/AnimateStack/local_components"
        os.makedirs(local_dir, exist_ok=True)
        
        filename = f"{component.slug}.json"
        file_path = os.path.join(local_dir, filename)
        
        file_data = {
            "title": component.title,
            "description": component.description,
            "code_content": component.code_content,
            "creator": component.creator.username,
            "created_at": str(component.created_at),
            "category": category.name if category else "Uncategorized"
        }
        
        with open(file_path, 'w') as f:
            json.dump(file_data, f, indent=4)
            
        component.local_path = file_path
        component.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, slug=None):
        from .models import Notification
        component = self.get_object()
        component.is_approved = True
        component.save()
        
        Notification.objects.create(
            user=component.creator,
            message=f"Congratulations! Your component '{component.title}' has been approved.",
            notification_type='success'
        )
        return Response({'status': 'approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, slug=None):
        from .models import Notification
        component = self.get_object()
        # We can either delete or just mark as rejected (not approved)
        # For now, let's keep it but maybe add a rejected flag later. 
        # Just sending notification.
        
        reason = request.data.get('reason', 'Does not meet quality standards.')
        
        Notification.objects.create(
            user=component.creator,
            message=f"Your component '{component.title}' was rejected. Reason: {reason}",
            notification_type='error'
        )
        return Response({'status': 'rejected'})

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
