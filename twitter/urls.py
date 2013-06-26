from django.conf.urls import *

urlpatterns = patterns('',
    # url(r'^login/', 'twitter.views.twitter_login'),
    url(r'^add_account/twitter', 'twitter.views.add_twitter_account'),
    url(r'^sayhello', 'twitter.views.tweeter'),
)