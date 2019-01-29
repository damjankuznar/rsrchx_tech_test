from django.contrib.auth import models
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = input("Enter username:")
        password = input("Enter password:")

        user = models.User.objects.create_user(username, password=password)
        user.is_superuser = False
        user.is_staff = False
        user.save()
