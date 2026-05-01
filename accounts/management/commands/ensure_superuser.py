import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from env vars if none exists"

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists, skipping.")
            return

        email = os.environ.get("SUPERUSER_EMAIL")
        password = os.environ.get("SUPERUSER_PASSWORD")

        if not email or not password:
            self.stdout.write(
                "SUPERUSER_EMAIL and SUPERUSER_PASSWORD not set, skipping."
            )
            return

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email, "role": "admin"},
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "created" if created else "promoted to superuser"
        self.stdout.write(self.style.SUCCESS(f"Superuser {email} {action}."))
