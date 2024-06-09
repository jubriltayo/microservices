from django.core.management.base import BaseCommand
from report_app.models import Report
from faker import Faker


class Command(BaseCommand):
    help = 'Populate the database with sample reports'

    def handle(self, *args, **kwargs):
        fake = Faker()

        for _ in range(10):
            title = fake.sentence(nb_words=6)
            content = fake.text(max_nb_chars=200)
            Report.objects.create(title=title, content=content)

        self.stdout.write(self.style.SUCCESS('Successfully populated'))