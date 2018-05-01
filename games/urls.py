from django.conf.urls import url
from games.views import BaseIndexView, OnlineTestView, AddTest, IndexView, \
    ChangeQuestionsView, UserResultsView, RightAnswerHalfView, TwoAnswerJokerView, \
    UserGameHistory, AboutUsView, ContactView, GameExitView, ShareFacebookWithFriends,\
    SocialResultsView, SharePlayerResultView, CeleryWorkerView, PlayerDashboard, \
    ExportAllQuestions, ListViewAllDocuments
from django.contrib.auth import views as auth_views
from django.conf import settings

urlpatterns = [
    url(r'^$', BaseIndexView.as_view(), name="index"),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout,  name="logout",  kwargs={'next_page': '/'}),
    url(r'^online/test/$', OnlineTestView.as_view(), name='test-online'),
    url(r'^dashboard/$', PlayerDashboard.as_view(), name='player-dashboard'),
    url(r'^game/exit/$', GameExitView.as_view(), name='game-exit'),
    url(r'^addtest/$', AddTest.as_view(), name='add-test'),
    url(r'^test/$', IndexView.as_view(), name='test-index'),
    # social urls
    url(r'^share/$', ShareFacebookWithFriends.as_view(), name='share-with-friends'),
    url(r'^share-result/$', SharePlayerResultView.as_view(), name='share-redirect-home'),
    url(r'^social/results/$', SocialResultsView.as_view(), name='share-results'),
    url(r'^question/change/$', ChangeQuestionsView.as_view(), name='change-question'),
    url(r'^question/half/$', RightAnswerHalfView.as_view(), name='half-question'),
    url(r'^question/two/$', TwoAnswerJokerView.as_view(), name='two-answer'),
    url(r'^results/$', UserResultsView.as_view(), name='result'),
    url(r'^history/$', UserGameHistory.as_view(), name='history'),
    url(r'^about-us/$', AboutUsView.as_view(), name='about-us'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^update_celery_worker/$', CeleryWorkerView.as_view(), name='worker-update'),
    url(r'^export/document/$', ExportAllQuestions.as_view(), name='export-question'),
    url(r'^admin/document/suallar/list/$', ListViewAllDocuments.as_view(), name='all-question-doc'),

]

