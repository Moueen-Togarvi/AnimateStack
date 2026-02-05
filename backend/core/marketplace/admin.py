from django.contrib import admin
from .models import Purchase, Review, Like, Comment, Collection

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'component', 'amount', 'created_at')
    search_fields = ('user__username', 'component__title', 'transaction_id')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'component', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'component', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'component', 'created_at')
    search_fields = ('text',)

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_public', 'created_at')
    list_filter = ('is_public',)
