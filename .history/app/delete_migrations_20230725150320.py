import os

import django.apps
from django.conf import settings
from django.core.management.base import BaseCommand


def delete_migrations(app):
    print(f"Deleting {app}'s migration files")
    migrations_dir = os.path.join(settings.BASE_DIR, f'apps{os.path.sep}{app}{os.path.sep}migrations')

    if os.path.exists(migrations_dir):
        for the_file in os.listdir(migrations_dir):
            file_path = os.path.join(migrations_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

            f = open(f"{os.path.join(migrations_dir, '__init__.py')}", "w")
            f.close()

    else:
        print('-' * 20, migrations_dir, 'does not exist')


class Command(BaseCommand):
    """
    Resets migrations and clears directories
    """
    help = 'reset migrations'

    def handle(self, *args, **options):
        set_of_apps = set()
        disregard = []

        # get all apps
        for model in django.apps.apps.get_models():
            if model._meta.app_label not in disregard:
                set_of_apps.add(model._meta.app_label)

        for app in set_of_apps:
            delete_migrations(app)