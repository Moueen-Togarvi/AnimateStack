from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Component, Category, Tag
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with sample components'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')

        # Create Admin User if not exists
        admin_user, created = User.objects.get_or_create(
            email='admin@animatestack.com',
            defaults={
                'username': 'admin',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user'))

        # Create Categories
        categories = ['Buttons', 'Cards', 'Inputs', 'Navigation', 'Feedback']
        for cat_name in categories:
            Category.objects.get_or_create(name=cat_name, slug=cat_name.lower())
        
        # Create Tags
        tags = ['modern', 'dark-mode', 'animated', 'minimal']
        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)

        # Sample Components
        components_data = [
            {
                'title': 'Neon Gradient Button',
                'description': 'A glowing button with gradient border and hover effects.',
                'category': 'Buttons',
                'code_content': {
                    'html': """
<button class="relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-purple-600 to-blue-500 group-hover:from-purple-600 group-hover:to-blue-500 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800">
    <span class="relative px-5 py-2.5 transition-all ease-in duration-75 bg-white dark:bg-gray-900 rounded-md group-hover:bg-opacity-0">
        Neon Button
    </span>
</button>
""",
                    'css': '',
                    'js': ''
                }
            },
            {
                'title': 'Glassmorphism Card',
                'description': 'Modern glass effect card with blur and transparency.',
                'category': 'Cards',
                'code_content': {
                    'html': """
<div class="max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800/50 dark:border-gray-700 backdrop-blur-sm">
    <a href="#">
        <h5 class="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">Glass Card</h5>
    </a>
    <p class="mb-3 font-normal text-gray-700 dark:text-gray-400">Here are the biggest enterprise technology acquisitions of 2021 so far, in reverse chronological order.</p>
    <a href="#" class="inline-flex items-center px-3 py-2 text-sm font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
        Read more
        <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 5h12m0 0L9 1m4 4L9 9"/>
        </svg>
    </a>
</div>
""",
                    'css': '',
                    'js': ''
                }
            }
        ]

        for comp_data in components_data:
            category = Category.objects.get(name=comp_data['category'])
            comp, created = Component.objects.get_or_create(
                title=comp_data['title'],
                defaults={
                    'description': comp_data['description'],
                    'code_content': comp_data['code_content'],
                    'category': category,
                    'creator': admin_user,
                    'is_public': True,
                    'price': 0.00
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created component: {comp.title}"))

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))
