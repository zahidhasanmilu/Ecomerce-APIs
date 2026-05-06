from django.core.management.base import BaseCommand
from django.db import transaction
import random
from faker import Faker
from decimal import Decimal

from products.models import Category, Product
from shop.models import Shop

fake = Faker()
NUM_PRODUCTS_PER_SHOP = 10
DISCOUNT_RANGE = [0, 5, 10, 15, 20, 25]
PRICE_RANGE = (500, 4000)
STOCK_RANGE = (50, 200)
DUMMY_IMAGE_PATH = "product/product-default.jpg"


class Command(BaseCommand):
    help = 'Populate DB with dummy Product data for active Shops.'

    def handle(self, *args, **options):
        with transaction.atomic():
            shops = list(Shop.objects.filter(status='active'))
            if not shops:
                self.stdout.write(
                    self.style.WARNING(
                        "🛑 No active Shops found. Please create Shops first."
                    )
                )
                return

            categories = list(Category.objects.all())
            if not categories:
                self.stdout.write(
                    self.style.WARNING(
                        "🛑 No Categories found. Please create Categories first."
                    )
                )
                return

            total_products_to_create = len(shops) * NUM_PRODUCTS_PER_SHOP
            self.stdout.write(f"\n--- Creating {total_products_to_create} Products ---")
            product_count = 0

            for shop in shops:
                for i in range(NUM_PRODUCTS_PER_SHOP):
                    product_count += 1

                    prod_title = (
                        f"{fake.color_name()} {fake.word().capitalize()} "
                        f"{fake.random_int(min=10, max=99)}"
                    )
                    while Product.objects.filter(title=prod_title).exists():
                        prod_title = (
                            f"{fake.color_name()} {fake.word().capitalize()} "
                            f"{fake.random_int(min=10, max=99)}"
                        )

                    try:
                        price_value = Decimal(random.randint(*PRICE_RANGE)).quantize(
                            Decimal('0.00')
                        )

                        Product.objects.create(
                            shop=shop,
                            category=random.choice(categories),
                            title=prod_title,
                            image=DUMMY_IMAGE_PATH,
                            description=fake.paragraph(nb_sentences=5),
                            price=price_value,
                            discount_percentage=random.choice(DISCOUNT_RANGE),
                            stock=random.randint(*STOCK_RANGE),
                            is_active=True,
                        )

                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✅ Product {product_count}/{total_products_to_create} "
                                f"created for Shop '{shop.name}'."
                            )
                        )

                    except Exception as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ Error creating product for Shop '{shop.name}': {e}"
                            )
                        )

            self.stdout.write("\n==============================================")
            self.stdout.write(
                self.style.SUCCESS("✨ Product Data Generation Completed Successfully!")
            )
            self.stdout.write("==============================================")
