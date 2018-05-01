from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.contrib.auth import get_user_model
from PIL import Image
from django.utils import timezone
import calendar
from django.db.models import Q

from base_user.tools.common import game_session_generate, current_week_range, current_month_range
from games.models import GameTime, WeekBoard, MonthBoard, WeeklyResults, MonthlyResults, LeaderResults, Question, Answer
from datetime import timedelta
import pandas as pd

User = get_user_model()


@shared_task
def GamePictureCropper(image):
    base_image = Image.open(image)
    width, height = base_image.size
    print(width, height)
    if width > height:
        left, top = int((width-height)/2),0
        right, bottom = int(height+left),height
        crop = base_image.crop((left, top, right, bottom))
        w, h = crop.size
        print(w, h)
        crop.save(image, quality=100)
        return "New width: {0} -> {1}; New height: {2} - {3}".format(width,w,height,h)
    elif height > width:
        left, top = 0,int((height-width)/2)
        right, bottom = width, int(width+top)
        crop = base_image.crop((left, top, right, bottom))
        w, h = crop.size
        print(w, h)
        crop.save(image, quality=100)
        return "New width: {0} -> {1}; New height: {2} - {3}".format(width,w,height,h)
    else:
        return "Width: {0}; Height: {1}".format(width,height)

@shared_task
def add(x, y):
    return x + y

@shared_task
def all_user_create_game_session(user_id):
    try:
        player = User.objects.get(id=user_id)
        player.game_session = game_session_generate()
        player.save()
        return "Successfuly create {0} user => {1} id".format(player.get_full_name(), player.game_session)
    except:
        return "Cannot create Game session id"


# @shared_task
# def leaderbord_count_week_and_month(user_id):
#     user = User.objects.get(id=user_id)
#     if not user.hide_leaderboard:
#         best_month = GameTime.objects.filter(player=user,done=True, game_time__range=current_month_range()).order_by('-answer_count','duration')
#         best_week = GameTime.objects.filter(player=user,done=True, game_time__range=current_week_range()).order_by('-answer_count','duration')
#
#         if best_week.first():
#             print("first week pass")
#             game_week = best_week.first()
#             if game_week.answer_count >= 8:
#                 print("Week point up to 8")
#                 try:
#                     week_test = WeekBoard.objects.get(games=game_week,week_name=str(current_week_range()))
#                     print("Already have week boards")
#                 except:
#                     week_game = WeekBoard(
#                         games=game_week,
#                         week_name=str(current_week_range())
#                     )
#                     week_game.save()
#                     print("Week game save to database")
#
#         if best_month:
#             print("Pass this month")
#             game_month = best_month.first()
#             if game_month.answer_count >= 8:
#                 print("Month point up to 8")
#                 try:
#                     month_test = MonthBoard.objects.get(games=game_month, month_name=str(current_month_range()))
#                     print("Already have this month result")
#                 except:
#                     month_game = MonthBoard(
#                         games=game_month,
#                         month_name=str(current_month_range())
#                     )
#                     month_game.save()
#                     print("Save to database Month results")
#
#         return "Celery Leader and Month boards Done !"
#     else:
#         return "This user cannot show leaderboard"


@shared_task
def leaderbord_count_week_and_month(user_id):
    user = User.objects.get(id=user_id)
    if not user.hide_leaderboard:
        best_month = GameTime.objects.filter(player=user, done=True, game_time__range=current_month_range()).order_by('-answer_count','duration')
        print(best_month)
        best_week = GameTime.objects.filter(player=user, done=True, game_time__range=current_week_range()).order_by('-answer_count','duration')
        print(best_week)
        if best_week.first():

            best_game_week_list = [game for game in best_week if game.answer_count > 7]
            total_score = 0
            total_time = timezone.timedelta(minutes=0, seconds=0)
            if best_game_week_list:
                print("Yes week game have")
                for week_game in best_game_week_list:
                    total_score += week_game.answer_count
                    total_time += week_game.duration
            print(total_score)
            print(total_time)

            week = WeekBoard.objects.filter(player=user, week_name=str(current_week_range()))
            if week.first():
                print("First objects")
                week_obj = week.first()
                week_obj.week_name = str(current_week_range())
                week_obj.duration = total_time
                week_obj.score = total_score
                week_obj.save()
                print("Object update")
            else:
                week_bord = WeekBoard(
                    player=user,
                    week_name=str(current_week_range()),
                    duration=total_time,
                    score=total_score
                )
                week_bord.save()
                print("Create new objects")
            # except:
            #     week_bord = WeekBoard(
            #         player=user,
            #         week_name=str(current_week_range()),
            #         duration=total_time,
            #         score=total_score
            #     )
            #     week_bord.save()
            #     print("Create")

        if best_month.first():
            print("Best month have")
            best_game_month_list = [game for game in best_month if game.answer_count > 7]
            total_month_score = 0
            total_month_time = timezone.timedelta(minutes=0, seconds=0)
            print(total_month_score)
            print(total_month_time)
            if best_game_month_list:
                for month_game in best_game_month_list:
                    total_month_score += month_game.answer_count
                    total_month_time += month_game.duration
            try:
                month = MonthBoard.objects.filter(player=user, month_name=str(current_month_range()))
                if month.first():
                    print("Month First objects")
                    month_obj = month.first()
                    month_obj.month_name = str(current_month_range())
                    month_obj.duration = total_month_time
                    month_obj.score = total_month_score
                    month_obj.save()
                    print("Month obj update")
                else:
                    month_bord = MonthBoard(
                        player=user,
                        month_name=str(current_month_range()),
                        duration=total_month_time,
                        score=total_month_score
                    )
                    month_bord.save()
                    print("Create new month")
            except:
                month_bord = MonthBoard(
                    player=user,
                    month_name=str(current_month_range()),
                    duration=total_month_time,
                    score=total_month_score
                )
                month_bord.save()
                print("Create new month")
        return "Celery Leader and Month boards Done !"
    else:
        return "This user cannot show leaderboard"


@shared_task
def calc_weekly():
    today = timezone.now()

    #today = timezone.now()  # because models saved on UTC timezone we don't need local timezone
    #start_date = timezone.datetime(today.year, today.month - 1, 25).replace(tzinfo=today.tzinfo)  # default
    start_date = today - timedelta(days=today.weekday(),minutes=today.minute, hours=int(today.hour))
    #end_date = timezone.datetime(today.year, today.month, 8,23,59).replace(tzinfo=today.tzinfo)
    end_date = start_date + timedelta(days=6, minutes=59, hours=23)
    if end_date.day == today.day and today.hour >= 20:
        new_week = today + timedelta(days=1)
        start_date = new_week - timedelta(days=new_week.weekday(), minutes=new_week.minute, hours=int(new_week.hour))
        # end_date = timezone.datetime(today.year, today.month, 8,23,59).replace(tzinfo=today.tzinfo)
        end_date = start_date + timedelta(days=6, minutes=59, hours=23)

    week_games = GameTime.objects.filter(Q(player__weekly_leaderboard=False),
                                         Q(game_time__gte=start_date - timedelta(hours=4)),
                                         Q(game_time__lte=end_date - timedelta(hours=4)),
                                         Q(done=True)).values('answer_count', 'player', 'duration')
    week_dtf = pd.DataFrame.from_records(week_games)
    weekly_table = week_dtf.groupby(['player']).agg({'answer_count': 'sum', 'duration': 'sum'})  #.reset_index()
    weekly_table = weekly_table.sort_values(['answer_count', 'duration'], ascending=[False, True]).head(n=10)
    # weekly_result = weekly_table.reset_index().to_dict(orient='records')
    weekly_result = weekly_table.reset_index().to_json(orient='records')
    weekly_board, created = WeeklyResults.objects.get_or_create(
        start=start_date.date(),
        end=end_date.date()
    )
    weekly_board.result = weekly_result
    weekly_board.save()
    return "Successfully Weekly Score bord updated"


@shared_task
def calc_monthly():
    # today = timezone.localtime(timezone.now())
    today = timezone.now()   # because models saved on UTC timezone we don't need local timezone
    last_day = calendar.monthrange(today.year, today.month)[1]
    start_date = timezone.datetime(today.year, today.month, 1, 0, 0)
    end_date = start_date + timedelta(days=last_day-1, minutes=59, hours=23)
    # end_date = calendar.monthrange(today.year, today.month)[1]
    if end_date.day == today.day and today.hour >= 20:
        next_month = today + timedelta(days=1)
        last_day = calendar.monthrange(next_month.year, next_month.month)[1]
        start_date = timezone.datetime(next_month.year, next_month.month, 1, 0, 0)
        end_date = start_date + timedelta(days=last_day - 1, minutes=59, hours=23)
    # start_date = timezone.datetime.strptime("{0}-{1}-{2}".format(today.year, today.month, start_date), '%Y-%m-%d')
    # start_date = start_date.replace(tzinfo=today.tzinfo)
    # end_date = timezone.datetime.strptime("{0}-{1}-{2}".format(today.year, today.month, end_date), '%Y-%m-%d')
    # end_date = end_date.replace(tzinfo=today.tzinfo)

    month_games = GameTime.objects.filter(Q(player__monthly_leaderboard=False),
                                          Q(game_time__gte=start_date - timedelta(hours=4)),
                                          Q(game_time__lte=end_date - timedelta(hours=4)),
                                          Q(game_time__month=today.month),
                                          Q(done=True)).values('answer_count', 'player', 'duration')
    month_dtf = pd.DataFrame.from_records(month_games)
    monthly_table = month_dtf.groupby(['player']).agg({'answer_count': 'sum', 'duration': 'sum'})  #.reset_index()
    monthly_table = monthly_table.sort_values(['answer_count', 'duration'], ascending=[False, True]).head(n=10)
    # monthly_result = monthly_table.reset_index().to_dict(orient='records')
    monthly_result = monthly_table.reset_index().to_json(orient='records')
    monthly_board, created = MonthlyResults.objects.get_or_create(
        start=start_date.date(),
        end=end_date.date()
    )
    monthly_board.result = monthly_result
    monthly_board.save()
    return "Successfully Monthly Score bord updated"

@shared_task
def calc_leaderbord():
    today = timezone.now()
    day_end = timezone.datetime(2017, 12, 31, 20, 0).replace(tzinfo=today.tzinfo)
    all_games = GameTime.objects.filter(player__hide_leaderboard=False, done=True, game_time__lte=day_end).values('answer_count', 'player', 'duration')
    games_dtf = pd.DataFrame.from_records(all_games)
    games_table = games_dtf.groupby(['player']).agg({'answer_count': 'sum', 'duration': 'sum'})  # .reset_index()
    games_table = games_table.sort_values(['answer_count', 'duration'], ascending=[False, True]).head(n=10)
    game_result = games_table.reset_index().to_json(orient='records')
    game_bord, created = LeaderResults.objects.get_or_create(
        name="all"
    )
    game_bord.result = game_result
    game_bord.save()
    return "All leaderbord updated"


@shared_task
def points_counter(user_id):
    user = User.objects.get(id=user_id)
    player_games = GameTime.objects.filter(player=user,done=True).values('answer_count')
    player_duration = GameTime.objects.filter(player=user,done=True).values('duration')
    point = 0
    duration_full_count = 0
    if player_games:
        games_dtf = pd.DataFrame.from_records(player_games)
        games_table = games_dtf.agg({'answer_count': 'sum'})
        games_table = games_table.reset_index().to_dict(orient='records')
        point = games_table[0][0] if games_table else 0
        duration_dtf = pd.DataFrame.from_records(player_duration)
        duration_count = duration_dtf.agg({'duration': 'sum'})
        duration_count = duration_count.reset_index().to_dict(orient='records')
        duration_full_count = duration_count[0][0] if duration_count else 0
    user.point = point
    today = timezone.now()
    start_date = today - timedelta(days=today.weekday(), minutes=today.minute, hours=int(today.hour + 4))
    end_date = start_date + timedelta(days=6, minutes=59, hours=23)
    if end_date.day == today.day and today.hour >= 20:
        new_week = today + timedelta(days=1)
        start_date = new_week - timedelta(days=today.weekday(), minutes=today.minute, hours=int(today.hour + 4))
        end_date = start_date + timedelta(days=6, minutes=59, hours=23)
        start_date = start_date - timedelta(hours=4)
        end_date = end_date - timedelta(hours=4)
    else:
        start_date = start_date - timedelta(hours=4)
        end_date = end_date - timedelta(hours=4)
    weekly_point_games = GameTime.objects.filter(Q(player=user),
                                                 Q(game_time__gte=start_date),
                                                 Q(game_time__lte=end_date),
                                                 Q(done=True)).values('answer_count')
    point_week = 0
    if weekly_point_games:
        weekly_games_dtf = pd.DataFrame.from_records(weekly_point_games)
        games_table_weekly = weekly_games_dtf.agg({'answer_count': 'sum'})
        games_table_weekly = games_table_weekly.reset_index().to_dict(orient='records')
        point_week = games_table_weekly[0][0] if games_table_weekly else 0
    user.point_week = point_week
    last_day = calendar.monthrange(today.year, today.month)[1]
    start_date_month = timezone.datetime(today.year, today.month, 1, 0, 0).replace(tzinfo=today.tzinfo) - timezone.timedelta(
        hours=4)
    end_date_month = start_date_month + timedelta(days=last_day - 1, minutes=59, hours=23)
    # end_date = calendar.monthrange(today.year, today.month)[1]
    if end_date_month.day == today.day and today.hour >= 20:
        next_month = today + timedelta(days=1)
        last_day = calendar.monthrange(next_month.year, next_month.month)[1]
        start_date_month = timezone.datetime(next_month.year, next_month.month, 1, 0, 0).replace(
            tzinfo=today.tzinfo)
        end_date = start_date_month + timedelta(days=last_day - 1, minutes=59, hours=23)
    else:
        pass
    monthly_point_games = GameTime.objects.filter(Q(player=user),
                                                  Q(game_time__gte=start_date_month),
                                                  Q(game_time__lte=end_date_month),
                                                  Q(done=True)).values('answer_count')
    point_monthly = 0
    if monthly_point_games:
        monthly_games_dtf = pd.DataFrame.from_records(monthly_point_games)
        games_table_monthly = monthly_games_dtf.agg({'answer_count': 'sum'})
        games_table_monthly = games_table_monthly.reset_index().to_dict(orient='records')
        point_monthly = games_table_monthly[0][0] if games_table_monthly else 0
    user.point_month = point_monthly
    user.full_duration = duration_full_count
    user.save()
    return "User points updated"


@shared_task
def question_answer_find():
    question_list = Question.objects.all()
    for question in question_list:
        right_answer = Answer.objects.filter(question=question, status=True).last()
        right_answer.answer += "(*)"
        right_answer.save()
    return print("Question count :", question_list.count())