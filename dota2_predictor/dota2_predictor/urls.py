from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dota2 import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dota2_predictor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^prediction/', views.prediction, name='prediction')
)

urlpatterns += staticfiles_urlpatterns()
