from django.core.management.base import BaseCommand
from games.models import Question
from games.tasks import GamePictureCropper
from django.conf import settings


class Command(BaseCommand):
    help = "This command automatically Update all image fields Questions model"

    def handle(self, *args, **options):
        print("started ...")
        all_questions = Question.objects.all()
        for question in all_questions:
            if question.image:
                path = "{}/{}".format(settings.MEDIA_ROOT,question.image)
                print(path)
                GamePictureCropper.delay(path)
        print("Done all objects : ", all_questions.count())