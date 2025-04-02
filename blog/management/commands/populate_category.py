from blog.models import Category
from django.core.management.base import BaseCommand
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Insert sample data into the category model"

    def handle(self, *args, **options):

        Category.objects.all().delete()

        categories=['sports','Technology','food','art','science']

        for categories_post in categories:
            Category.objects.create(name=categories_post)


        self.stdout.write(self.style.SUCCESS("Successfully inserted sample posts"))
