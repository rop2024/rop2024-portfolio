from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Create admin user if it doesn\'t exist'

    def handle(self, *args, **options):
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.getenv('ADMIN_PASSWORD')

        if not admin_password:
            self.stdout.write(
                self.style.WARNING('ADMIN_PASSWORD not set. Skipping admin user creation.')
            )
            return

        if User.objects.filter(username=admin_username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Admin user "{admin_username}" already exists.')
            )
            return

        User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user "{admin_username}".')
        )