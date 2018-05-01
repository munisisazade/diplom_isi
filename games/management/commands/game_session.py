from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from games.tasks import all_user_create_game_session
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    help = "This command automatically Create game session id for all users"

    def handle(self, *args, **options):
        print("started ...")
        all_users = User.objects.all()
        for user in all_users:
            all_user_create_game_session(user.id)
            print("%s -- Done" % user.get_full_name() if user.get_full_name() else user.username)
        print("Done all objects : ", all_users.count())