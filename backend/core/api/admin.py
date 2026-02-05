from django.contrib import admin
from .models import Component, Category, Tag, Asset, Notification

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'is_public', 'is_approved', 'created_at')
    list_filter = ('is_public', 'is_approved', 'category')
    search_fields = ('title', 'description', 'creator__username')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('file', 'asset_type', 'uploaded_by', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')
