import csv

from django.conf import settings
from django.db import Error
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Uploading files to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ingredients',
            action='store_true',
            help='add_ingredients',
        )

    def handle(self, *args, **options):
        if options['ingredients']:
            path = settings.MEDIA_ROOT + '/data/ingredients.csv'
            with open(path, 'r', newline='') as ingredients:
                ingredients = csv.reader(ingredients)
                try:
                    for ingredient in ingredients:
                        Ingredient.objects.create(
                            name=ingredient[0], measurement_unit=ingredient[1])
                    self.stdout.write(self.style.SUCCESS(
                        'File ingredients.csv uploaded '
                        'in database successfully'
                    ))
                except Error:
                    raise CommandError(
                        'Some error occurred while '
                        'creating the object "ingredient"'
                    )
