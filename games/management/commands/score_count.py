from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.tasks import points_counter

User = get_user_model()


class Command(BaseCommand):
    help = "This command automatically Create score all points"

    def handle(self, *args, **options):
        print("started ...")
        all_users = User.objects.all()
        for user in all_users:
            points_counter(user.id)
        print("Done all objects : ", all_users.count())