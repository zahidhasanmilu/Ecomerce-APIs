# shop/management/commands/populate_shops.py
from django.core.management.base import BaseCommand
from shop.models import Shop
from account.models import User
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = "Populate DB with dummy Shop data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of shops to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        users = list(User.objects.all())
        if not users:
            self.stdout.write(
                self.style.WARNING("No Users found. Please create User accounts first.")
            )
            return

        self.stdout.write(f"Creating {count} dummy shops...")

        for _ in range(count):
            try:
                owner = random.choice(users)
                shop_name = "BRAND " + fake.company() + str(random.randint(10, 99))
                while Shop.objects.filter(name=shop_name).exists():
                    shop_name = "BRAND " + fake.company() + str(random.randint(10, 99))

                shop = Shop(
                    owner=owner,
                    name=shop_name,
                    tagline=fake.catch_phrase(),
                    description=fake.text(max_nb_chars=300),
                    contact_email=fake.email(),
                    contact_phone=fake.phone_number(),
                    address=fake.address(),
                    status=random.choice(["active", "pending", "inactive"]),
                    is_verified=random.choice([True, False]),
                )
                shop.save()
                self.stdout.write(self.style.SUCCESS(f"Shop '{shop_name}' created."))
            except Exception:
                continue

        self.stdout.write(
            self.style.SUCCESS(f"--- {count} dummy shops created successfully! ---")
        )
