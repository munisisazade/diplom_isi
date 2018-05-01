from django.views.generic import View
from games.models import GameTime
from django.contrib.auth import get_user_model
from base_user.tools.common import game_session_generate
from games.models import LeaderBoard
import facebook

User = get_user_model()

class UserGameSessionIdCheck(View):
    """
        Check user session id for game
    """

    def get_context_data(self, **kwargs):
        context = {}
        try:
            user = User.objects.get(id=self.request.user.id)
            if user.game_session:
                game_list = GameTime.objects.filter(game_session=user.game_session)
                if game_list:
                    for game in game_list:
                        game.done = True
                        game.last_done = True
                        game.save()
                        game.player.game_session = game_session_generate()
                        game.player.save()
                else:
                    pass
            else:
                pass
        except:
            pass
        return context

# def CheckLeaderBorad(game):
#     try:
#         if not game.player.hide_leaderboard:
#             leader = LeaderBoard.objects.filter(games__player=game.player).last()
#             count = LeaderBoard.objects.filter(games__player=game.player).count()
#             if count > 1:
#                 for obj in LeaderBoard.objects.filter(games__player=game.player)[:count-1]:
#                     obj.delete()
#             if leader.games.answer_count > game.answer_count:
#                 pass
#             else:
#                 if leader.games.duration > game.duration:
#                     leader.games = game
#                     leader.save()
#                 else:
#                     pass
#         else:
#             pass
#     except:
#         if not game.player.hide_leaderboard:
#             if game.answer_count > 7:
#                 leader = LeaderBoard(games=game)
#                 leader.save()
#             else:
#                 pass
#         else:
#             pass

def CheckLeaderBorad(game):
    try:
        if not game.player.hide_leaderboard:
            leader = LeaderBoard.objects.filter(player=game.player).last()
            count = LeaderBoard.objects.filter(player=game.player).count()
            if count > 1:
                for obj in LeaderBoard.objects.filter(player=game.player)[:count-1]:
                    obj.delete()
            if game.answer_count > 7:
                leader.duration += game.duration
                leader.score += game.answer_count
                leader.save()
            else:
                pass
        else:
            pass
    except:
        if not game.player.hide_leaderboard:
            if game.answer_count > 7:
                leader = LeaderBoard(
                    player=game.player,
                    duration=game.duration,
                    score=game.answer_count
                )
                leader.save()
            else:
                pass
        else:
            pass


def increase_point(user):
    result = user.count_point()
    user.point = result[0]
    user.point_month = result[1]
    user.point_week = result[2]
    user.save()


"""
    Check User Friends Have also use app
    from django.contrib.auth import get_user_model
    import facebook
    
    User = get_user_model()
    player = User.objects.filter(id=user_id)
    facebook_user = player.social_auth.get(provider='facebook')
    access_token = facebook_user.get_access_token("facebook") # get user access token
    facebook_uuid = facebook_user.uid
    graph = facebook.GraphAPI(access_token)
    resp = graph.get_object(facebook_uuid + '/friends') # get friends data
    data = resp['data']
"""

class FacebookFriendsList(object):
    def __init__(self, user):
        self.user = user

    def get_user_friends(self):
        try:
            facebook_user = self.user.social_auth.get(provider='facebook')
            access_token = facebook_user.get_access_token("facebook")  # get user access token
            facebook_uuid = facebook_user.uid
            graph = facebook.GraphAPI(access_token)
            resp = graph.get_object(facebook_uuid + '/friends')  # get friends data
            data = resp['data']
            return data
        except:
            return None