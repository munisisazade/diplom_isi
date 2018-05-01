from django.contrib import admin
from games.models import Answer, Question, UserQuestionHistory, GameTime, LeaderBoard, \
    WebsiteHeader, WeeklyResults, MonthlyResults, LeaderResults

# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 4
        return max_num


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInline,
    ]
    search_fields = ('question',)
    readonly_fields = ('get_excell',)
    list_display = ('question', 'get_excell','right_answer')


class UserQuestionHistoryAdmin(admin.ModelAdmin):
    list_filter = ('player_game__player', 'answer', 'date')
    list_display = ('player_game','question_id', 'answer', 'date')


class GameTimeAdmin(admin.ModelAdmin):
    list_filter = ('answer_count', 'game_time', 'player')
    list_display = ('player_name', 'answer_count', 'duration','game_time')

class WeeklyResultsAdmin(admin.ModelAdmin):
    list_display = ('week_name', 'week_time', 'get_week_winners')
    readonly_fields = ('week_liders',)
    fields = ('week_liders',)

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js',  # jquery
        )

class MonthlyResultsAdmin(admin.ModelAdmin):
    list_display = ('month_name', 'month_time', 'get_month_winners')
    readonly_fields = ('month_liders',)
    fields = ('month_liders',)

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js',  # jquery
        )

class LidersAllResultsAdmin(admin.ModelAdmin):
    list_display = ('get_name',  'get_winners')
    readonly_fields = ('get_liders',)
    fields = ('get_liders',)

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js',  # jquery
        )

admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuestionHistory, UserQuestionHistoryAdmin)
admin.site.register(GameTime, GameTimeAdmin)
# admin.site.register(LeaderBoard)
admin.site.register(WebsiteHeader)
# admin.site.register(MonthBoard)
# admin.site.register(WeekBoard)
admin.site.register(LeaderResults, LidersAllResultsAdmin)
admin.site.register(WeeklyResults, WeeklyResultsAdmin)
admin.site.register(MonthlyResults, MonthlyResultsAdmin)
