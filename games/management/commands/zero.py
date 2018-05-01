from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.tasks import leaderbord_count_week_and_month

User = get_user_model()


class Command(BaseCommand):
    help = "This command automatically Delete all points"

    def handle(self, *args, **options):
        print("started ...")
        all_users = User.objects.all()
        for user in all_users:
            user.point = 0
            user.point_month = 0
            user.point_week = 0
            user.save()
        print("Done all objects : ", all_users.count())