from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True) # Lucide icon name

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Component(models.Model):
    FRAMEWORK_CHOICES = (
        ('html', 'HTML/CSS'),
        ('react', 'React'),
        ('vue', 'Vue'),
        ('svelte', 'Svelte'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    code_content = models.JSONField(default=dict) # { "html": "...", "css": "...", "js": "..." }
    preview_url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='components')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='components')
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Stats
    views = models.PositiveIntegerField(default=0)
    downloads = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_components', blank=True)

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Asset(models.Model):
    ASSET_TYPES = (
        ('3d', '3D Model (GLTF/GLB)'),
        ('image', 'Image'),
        ('lottie', 'Lottie Animation'),
    )

    file = models.FileField(upload_to='assets/')
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES, default='3d')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_type} - {self.file.name}"
