import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

email = 'admin@animatestack.com'
password = 'adminpassword123'
username = 'admin'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser created: {email} / {password}")
else:
    print(f"Superuser already exists: {email}")
