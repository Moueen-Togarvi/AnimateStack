from django.core.management.base import BaseCommand
from api.models import Category, Component, User
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        # Create Categories
        categories = [
            {'name': 'Buttons', 'icon': '🔘', 'slug': 'buttons'},
            {'name': 'Cards', 'icon': '🃏', 'slug': 'cards'},
            {'name': 'Loaders', 'icon': '⏳', 'slug': 'loaders'},
            {'name': 'Inputs', 'icon': '⌨️', 'slug': 'inputs'},
            {'name': 'Navigation', 'icon': '🧭', 'slug': 'navigation'},
            {'name': 'Backgrounds', 'icon': '✨', 'slug': 'backgrounds'},
        ]

        for cat_data in categories:
            Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'icon': cat_data['icon']}
            )
        
        self.stdout.write(self.style.SUCCESS('Categories created successfully'))

        # Ensure Admin User exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@animatestack.com', 'adminpassword123')
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        
        admin_user = User.objects.get(username='admin')

        # Create Sample Components
        components = [
            {
                'title': 'Neon Gradient Button',
                'description': 'A glowing neon button with gradient hover effects.',
                'category': 'Buttons',
                'code_content': {
                    "html": "<button class=\"relative px-6 py-3 font-bold text-white rounded-lg group\">\n<span class=\"absolute inset-0 w-full h-full transition duration-300 transform -translate-x-1 -translate-y-1 bg-purple-800 ease opacity-80 group-hover:translate-x-0 group-hover:translate-y-0\"></span>\n<span class=\"absolute inset-0 w-full h-full transition duration-300 transform translate-x-1 translate-y-1 bg-pink-800 ease opacity-80 group-hover:translate-x-0 group-hover:translate-y-0 mix-blend-screen\"></span>\n<span class=\"relative\">Button Text</span>\n</button>",
                    "css": "",
                    "js": ""
                }
            },
            {
                'title': 'Glassmorphism Card',
                'description': 'Modern glassmorphism effect card with blur and transparency.',
                'category': 'Cards',
                'code_content': {
                    "html": "<div class=\"w-80 h-96 bg-white/10 backdrop-blur-lg rounded-xl border border-white/20 shadow-xl p-6 flex flex-col justify-between\">\n<div class=\"h-1/2 bg-gradient-to-br from-indigo-500/30 to-purple-500/30 rounded-lg\"></div>\n<div>\n<h3 class=\"text-xl font-bold text-white mb-2\">Glass Card</h3>\n<p class=\"text-gray-300 text-sm\">This is a beautiful glassmorphism card using Tailwind CSS backdrop-blur utilities.</p>\n</div>\n<button class=\"w-full py-2 bg-white/20 hover:bg-white/30 text-white rounded-lg transition-colors\">Learn More</button>\n</div>",
                    "css": "body { background: #111; }",
                    "js": ""
                }
            }
        ]

        for comp_data in components:
            cat = Category.objects.get(name=comp_data['category'])
            Component.objects.get_or_create(
                title=comp_data['title'],
                defaults={
                    'description': comp_data['description'],
                    'category': cat,
                    'creator': admin_user,
                    'code_content': comp_data['code_content'],
                    'is_approved': True,
                    'is_public': True
                }
            )

        self.stdout.write(self.style.SUCCESS('Sample components created successfully'))
