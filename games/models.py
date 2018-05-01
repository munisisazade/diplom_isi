from datetime import timedelta

from django.db import models
from django.utils import timezone
from base_user.tools.common import get_question_photo, get_answer_photo, get_random_answer, check_week
from django.contrib.postgres.fields import JSONField
import base_user



class WebsiteHeader(models.Model):
    title = models.CharField(max_length=255, default="25 İLLİK FƏALİYYƏT, BİR ƏSRLİK NƏAİYYƏT")
    sub_text = models.TextField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    instagram_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title if self.title else "None"


# Create your models here.
class Question(models.Model):
    question = models.TextField(default="")
    image = models.ImageField(upload_to=get_question_photo, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Sual'
        verbose_name_plural = 'Suallar'

    def __str__(self):
        return "%s" % self.question

    def right_answer(self):
        return "<b>%s<b>" % Answer.objects.filter(question=self, status=True).last().answer if Answer.objects.filter(
            question=self, status=True).last() else "Yoxdur"

    right_answer.short_description = "Doğru cavab"
    right_answer.allow_tags = True

    def get_answer(self):
        return Answer.objects.filter(question=self).order_by("?")

    def get_true_answer(self):
        answer_list = Answer.objects.filter(question=self)
        return [a.id for a in answer_list if a.status] + [
            [b.id for b in answer_list if not b.status][get_random_answer()]]

    def get_excell(self):
        return "<a href='/admin/document/suallar/list/'>Yüklə</a>"
    get_excell.short_description = "Word formati"
    get_excell.allow_tags = True


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    question = models.ForeignKey('Question')
    image = models.ImageField(upload_to=get_answer_photo, null=True, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % self.answer


class GameTime(models.Model):
    player = models.ForeignKey('base_user.MyUser')
    duration = models.DurationField(default=timezone.timedelta(minutes=0, seconds=0))
    game_time = models.DateTimeField(auto_now_add=True)
    change_question_joker = models.BooleanField(default=False)
    half_question_joker = models.BooleanField(default=False)
    two_question_joker = models.BooleanField(default=False)
    two_question_joker_expired = models.BooleanField(default=False)
    game_session = models.CharField(max_length=200, null=True, blank=True)
    done = models.BooleanField(default=False)
    answer_count = models.IntegerField(default=0)
    last_done = models.BooleanField(default=False)
    over = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.player.get_full_name()

    def player_name(self):
        return "%s" % self.player.get_full_name()

    player_name.short_description = 'Oyunçu adı'
    player_name.allow_tags = True

    def get_last_answer(self):
        return UserQuestionHistory.objects.filter(player_game=self).order_by('id').last()

    def get_right_answer_count(self):
        return UserQuestionHistory.objects.filter(player_game=self, answer=True).count()

    get_right_answer_count.short_description = "Düzgün cavabların sayı"
    get_right_answer_count.allow_tags = True


class UserQuestionHistory(models.Model):
    player_game = models.ForeignKey('GameTime', null=True, blank=True)
    question = models.ForeignKey('Question')
    answer = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.answer

class Repeating(models.Model):
    player = models.ForeignKey('base_user.MyUser')
    question = models.ForeignKey('Question')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.player.get_full_name()


class LeaderBoard(models.Model):
    games = models.ForeignKey('GameTime', null=True, blank=True)
    player = models.ForeignKey('base_user.MyUser', null=True, blank=True)
    duration = models.DurationField(default=timezone.timedelta(minutes=0, seconds=0))
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.player.get_full_name()


class MonthBoard(models.Model):
    games = models.ForeignKey('GameTime', null=True, blank=True)
    player = models.ForeignKey('base_user.MyUser', null=True, blank=True)
    duration = models.DurationField(default=timezone.timedelta(minutes=0, seconds=0))
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    month_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.player.get_full_name()


class WeekBoard(models.Model):
    games = models.ForeignKey('GameTime', null=True, blank=True)  # ignore this
    player = models.ForeignKey('base_user.MyUser', null=True, blank=True)
    duration = models.DurationField(default=timezone.timedelta(minutes=0, seconds=0))
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    week_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.player.get_full_name()


class WeeklyResults(models.Model):
    result = JSONField(null=True, blank=True)
    start = models.DateField()
    end = models.DateField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Həftəlik nəticə'
        verbose_name_plural = 'Həftəlik nəticələr'

    def __str__(self):
        return "{} - {}".format(self.start, self.end)

    def week_liders(self):
        # button = "<button class='button-%s'>Nəticəyə bax</button>" % self.end
        html = "<ol>"
        liders = []
        weekly_result = eval(self.result) if self else []
        weekly_users = base_user.models.MyUser.objects.filter(id__in=[p['player'] for p in weekly_result])
        for x in weekly_result:
            liders.append("<li style='font-size:18px;'>{0} | <a href='https://www.facebook.com/{1}' target='_blank'>FB</a> | Xal:{2} Vaxt: {3}</li>".format(weekly_users.get(id=x['player']).get_full_name(),weekly_users.get(id=x['player']).social_auth.get(provider='facebook').uid, x['answer_count'], self.parse_duration(x['duration'])))
        end_html = "</ol>"
        # script = "<script>$(document).ready(function(){$('button-%s').click(function(e){e.preventDefault();$('ol').toggle(1000);});});</script>" % self.end
        output = html + "".join(liders) + end_html
        return output

    week_liders.short_description = "Həftənin qalibləri"
    week_liders.allow_tags = True

    def get_week_winners(self):
        return "<a href='{}/change/' class='default'>Həftənin qalibləri</a>".format(self.id)

    get_week_winners.short_description = "Qaliblər siyahısı"
    get_week_winners.allow_tags = True

    def week_time(self):
        return "{} - {}".format(self.start, self.end)

    week_time.short_description = "Tarix aralığı"
    week_time.allow_tags = True

    def week_name(self):
        try:
            data = check_week(self.start)
        except:
            data = "1 ci həftə"
        return data

    week_name.short_description = "Həftə"
    week_name.allow_tags = True

    def parse_duration(self, value):
        try:
            return str(timedelta(milliseconds=value))
        except:
            pass


class MonthlyResults(models.Model):
    result = JSONField(null=True, blank=True)
    start = models.DateField()
    end = models.DateField()

    class Meta:
        ordering = ('id',)
        verbose_name = 'Aylıq nəticə'
        verbose_name_plural = 'Aylıq nəticələr'

    def __str__(self):
        return "{} - {}".format(self.start, self.end)

    def month_liders(self):
        # button = "<button class='button-%s'>Nəticəyə bax</button>" % self.end
        html = "<ol>"
        liders = []
        monthly_result = eval(self.result) if self else []
        monthly_users = base_user.models.MyUser.objects.filter(id__in=[p['player'] for p in monthly_result])
        for x in monthly_result:
            liders.append("<li style='font-size:18px;'>{0} | <a href='https://www.facebook.com/{1}' target='_blank'>FB</a> | Xal:{2} Vaxt: {3}</li>".format(monthly_users.get(id=x['player']).get_full_name(),monthly_users.get(id=x['player']).social_auth.get(provider='facebook').uid, x['answer_count'], self.parse_duration(x['duration'])))
        end_html = "</ol>"
        output = html + "".join(liders) + end_html
        return output

    month_liders.short_description = "Aylıq qaliblər"
    month_liders.allow_tags = True

    def get_month_winners(self):
        return "<a href='{}/change/' class='default'>Ayın qalibləri</a>".format(self.id)

    get_month_winners.short_description = "Qaliblər siyahısı"
    get_month_winners.allow_tags = True

    def month_time(self):
        return "{} - {}".format(self.start, self.end)

    month_time.short_description = "Tarix aralığı"
    month_time.allow_tags = True

    def month_name(self):
        try:
            data = self.start.strftime("%B")
        except:
            data = "1 ci həftə"
        return data

    month_name.short_description = "Aylar"
    month_name.allow_tags = True

    def parse_duration(self, value):
        try:
            return str(timedelta(milliseconds=value))
        except:
            pass


class LeaderResults(models.Model):
    result = JSONField(null=True, blank=True)
    name = models.CharField(max_length=255, default="all")

    def __str__(self):
        return "Dekabrın 31 nə qədər olan nəticə"

    class Meta:
        ordering = ('id',)
        verbose_name = 'Yekun nəticə'
        verbose_name_plural = 'Yekun nəticələr'

    def get_liders(self):
        # button = "<button class='button-%s'>Nəticəyə bax</button>" % self.end
        html = "<ol>"
        liders = []
        lider_result = eval(self.result) if self else []
        lider_users = base_user.models.MyUser.objects.filter(id__in=[p['player'] for p in lider_result])
        for x in lider_result:
            liders.append("<li style='font-size:18px;'>{0} | <a href='https://www.facebook.com/{1}' target='_blank'>FB</a> | Xal:{2} Vaxt: {3}</li>".format(lider_users.get(id=x['player']).get_full_name(),lider_users.get(id=x['player']).social_auth.get(provider='facebook').uid, x['answer_count'], self.parse_duration(x['duration'])))
        end_html = "</ol>"
        output = html + "".join(liders) + end_html
        return output

    get_liders.short_description = "Yekun qaliblər"
    get_liders.allow_tags = True

    def get_winners(self):
        return "<a href='{}/change/' class='default'>Yekun qaliblər</a>".format(self.id)

    get_winners.short_description = "Qaliblər siyahısı"
    get_winners.allow_tags = True

    def get_name(self):
        return "Dekabrın 31 nə qədər olan nəticə"

    get_name.short_description = "Yekun"
    get_name.allow_tags = True

    def parse_duration(self, value):
        try:
            return str(timedelta(milliseconds=value))
        except:
            pass