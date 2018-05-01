from django.db.models.signals import post_save, pre_delete
from django.conf import settings
from django.dispatch import receiver
from games.models import GameTime, LeaderBoard, Question
from games.tasks import GamePictureCropper, calc_monthly, calc_weekly, calc_leaderbord, points_counter
from base_user.models import MyUser
from base_user.tools.common import game_session_generate
import logging
import os

logr = logging.getLogger(__name__)

@receiver(post_save,sender=GameTime,dispatch_uid='add_player_score')
def add_player_score(sender,**kwargs):
    pass
    # game = kwargs.get('instance')
    # if not game.player.hide_leaderboard:
    #     if game.answer_count >= 8 and not game.last_done:
    #         game.answer_count = game.get_right_answer_count()
    #         if game.done:
    #             game.last_done = True
    #         game.save()
    #         try:
    #             if not game.player.hide_leaderboard:
    #                 leader = LeaderBoard.objects.filter(player=game.player).last()
    #                 count = LeaderBoard.objects.filter(player=game.player).count()
    #                 if count > 1:
    #                     for obj in LeaderBoard.objects.filter(player=game.player)[:count - 1]:
    #                         obj.delete()
    #                 if game.answer_count > 7:
    #                     leader.duration += game.duration
    #                     leader.score += game.answer_count
    #                     leader.save()
    #                 else:
    #                     pass
    #             else:
    #                 pass
    #         except:
    #             if not game.player.hide_leaderboard:
    #                 if game.answer_count > 7:
    #                     leader = LeaderBoard(
    #                         player=game.player,
    #                         duration=game.duration,
    #                         score=game.answer_count
    #                     )
    #                     leader.save()
    #                 else:
    #                     pass
    #             else:
    #                 pass
    # else:
    #     pass


# @receiver(post_save,sender=Question,dispatch_uid='crop_image_task')
# def crop_image_task(sender,**kwargs):
#     question = kwargs.get('instance')
#     if question.image:
#         image_path = "{}/{}".format(settings.MEDIA_ROOT, question.image)
#         logr.debug(image_path)
#         GamePictureCropper.delay(image_path)


@receiver(post_save, sender=MyUser, dispatch_uid='create_game_session')
def create_game_session(sender, created ,**kwargs):
    pass
    # user = kwargs.get('instance')
    # try:
    #     result = user.count_point()
    #     user.point = result[0]
    #     user.point_month = result[1]
    #     user.point_week = result[2]
    #     user.save()
    # except:
    #     pass
    # if not user.game_session and created:
    #     user.game_session = game_session_generate()
    #     user.save()



@receiver(post_save, sender=GameTime, dispatch_uid='calc_scoreboards')
def calculate_scoreboards(sender, created ,**kwargs):
    game = kwargs.get('instance')
    if game.done:
        calc_monthly.delay()
        calc_weekly.delay()
        calc_leaderbord.delay()
        # user points counter
        points_counter.delay(game.player.id)
