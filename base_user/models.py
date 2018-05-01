from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from base_user.tools.common import get_user_profile_photo_file_name, GENDER, current_month_range, current_week_range
from games.models import GameTime
from datetime import datetime as d, timedelta
import calendar
from django.db.models import Q
# My custom tools import



# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL
import random


# Customize User model
class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=100, unique=True,
                                help_text=_('Tələb olunur. 75 simvol və ya az. Hərflər, Rəqəmlər və '
                                            '@/./+/-/_ simvollar.'),
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$', _('Düzgün istifadəçi adı daxil edin.'),
                                                              'yanlışdır')
                                ])
    first_name = models.CharField(_('first name'), max_length=255, blank=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True)
    email = models.EmailField(_('email address'), max_length=255)
    profile_picture = models.ImageField(upload_to=get_user_profile_photo_file_name, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER, verbose_name="cinsi", null=True, blank=True)
    point = models.IntegerField(default=0)
    point_month = models.IntegerField(default=0)
    point_week = models.IntegerField(default=0)
    aditional_chance = models.BooleanField(default=False, help_text="Əlavə oyun oynamağını təmin edir. Oyun sayı əlavə edən zaman aktivləşdirmək vacibdir")
    aditional_games_count = models.IntegerField(default=0, help_text="Əlavə oyunların sayı")
    full_duration = models.CharField(max_length=255, null=True, blank=True)
    social_share_count = models.IntegerField(default=0)
    share_time = models.CharField(max_length=255, null=True, blank=True)
    unlimited = models.BooleanField(default=False, help_text="Limitsiz oynaya bilər")
    weekly_leaderboard = models.BooleanField(default=False, help_text="Bu istifadəçi Həftəlik Liderborda düşmür")
    monthly_leaderboard = models.BooleanField(default=False, help_text="Bu istifadəçi Aylıq Liderborda düşmür")
    hide_leaderboard = models.BooleanField(default=False, help_text="Bu istifadəçi Liderborda düşmür")
    result_num = models.IntegerField(default=1)
    game_session = models.CharField(max_length=30, null=True, blank=True)
    exclude_question = models.TextField(default="[]")
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    """
        Important non-field stuff
    """
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'İstifadəçi'
        verbose_name_plural = 'İstifadəçilər'

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def count_point(self):
        games = GameTime.objects.filter(player=self)
        point_sum = 0
        if games.last():
            for point_list in games:
                point_sum += point_list.answer_count if point_list.answer_count > 7 else 0
        self.point = point_sum
        print(point_sum)
        game_month = GameTime.objects.filter(player=self,game_time__range=current_month_range())
        point_month_sum = 0
        if game_month.last():
            for point_month_list in game_month:
                point_month_sum += point_month_list.answer_count if point_month_list.answer_count > 7 else 0
        self.point_month = point_month_sum
        print(point_month_sum)
        point_week_sum = 0
        game_week = GameTime.objects.filter(player=self, game_time__range=current_week_range())
        if game_week.last():
            for point_week_list in game_week:
                point_week_sum += point_week_list.answer_count if point_week_list.answer_count > 7 else 0
        self.point_week = point_week_sum
        print(point_week_sum)
        return [point_sum, point_month_sum, point_week_sum]

    def count(self):
        try:
            current_time = timezone.now()
            if current_time.hour >= 20:
                day_start = timezone.datetime(current_time.year,
                                              current_time.month,
                                              current_time.day,
                                              20,
                                              0).replace(tzinfo=current_time.tzinfo)
                day_end = timezone.datetime(current_time.year,
                                            current_time.month,
                                            current_time.day + 1,
                                            20,
                                            0).replace(tzinfo=current_time.tzinfo)
            else:
                day_start = timezone.datetime(current_time.year,
                                              current_time.month,
                                              current_time.day - 1,
                                              20,
                                              0).replace(tzinfo=current_time.tzinfo)
                day_end = timezone.datetime(current_time.year,
                                            current_time.month,
                                            current_time.day,
                                            20,
                                            0).replace(tzinfo=current_time.tzinfo)
            count = GameTime.objects.filter(Q(player=self),
                                            Q(game_time__gte=day_start),
                                            Q(game_time__lte=day_end)).count()
            return count
        except:
            return 0


class UserConfrimationKeys(models.Model):
    key = models.CharField(max_length=255,null=True, blank=True)
    user = models.ForeignKey('MyUser', null=True,blank=True)
    expired = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date',)
        verbose_name = "Təstiqlənmiş user"
        verbose_name_plural = "Təstiqlənmiş userlər"

    def __str__(self):
        return "%s" % self.key