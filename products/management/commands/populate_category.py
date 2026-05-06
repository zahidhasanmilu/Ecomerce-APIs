from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = '6-ti basic product category database-e populate korbe'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Electronics', 'description': 'Gadgets and electronic devices'},
            {'name': 'Fashion', 'description': 'Clothing and apparel'},
            {'name': 'Home & Garden', 'description': 'Furniture and home decor'},
            {'name': 'Beauty', 'description': 'Skincare and cosmetic products'},
            {'name': 'Sports', 'description': 'Fitness gear and sports equipment'},
            {'name': 'Books', 'description': 'Educational and fictional books'},
        ]

        self.stdout.write("Populating categories...")

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Successfully created: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category already exists: {category.name}"))

        self.stdout.write(self.style.SUCCESS("All categories processed!"))