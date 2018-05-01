"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
# if you have multilang website uncomment
# from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns  # for url translation
# from oscar.app import application # oscar applications urls here


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include("games.urls")),
    url(r'^page/', include('django.contrib.flatpages.urls')),
    # path('social-login/', include('social_django.urls', namespace='social')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
]
# if you have multilang website uncomment
# urlpatterns += i18n_patterns(
#     url(r'^', include("games.urls")),
#     url(r'^', application.urls),
#     url(r'^page/', include('django.contrib.flatpages.urls')),
# )



# handler404 = 'game.views.NotFoundPage.as_view'


# This is change default admin panel Headers and titles
admin.site.site_header = 'Diplom Admin'
admin.site.site_title = 'Diplom Administration'
admin.site.index_title = 'Diplom Administration'

