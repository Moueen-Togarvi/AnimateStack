from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_creator = models.BooleanField(default=False)
    
    # Social Links
    github_handle = models.CharField(max_length=50, blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
