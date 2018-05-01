from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.tasks import question_answer_find

User = get_user_model()


class Command(BaseCommand):
    help = "Know all questions answer"

    def handle(self, *args, **options):
        print("started ...")
        question_answer_find.delay()
        print("Done all objects : ", "Question")