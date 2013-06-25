from django.conf.urls import *

urlpatterns = patterns('',
    # url(r'^login/', 'twitter.views.twitter_login'),
    url(r'^sayhello', 'twitter.views.tweeter'),
)