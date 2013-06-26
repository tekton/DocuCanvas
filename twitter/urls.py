from django.conf.urls import *

urlpatterns = patterns('',
    # url(r'^login/', 'twitter.views.twitter_login'),
    url(r'^add_account', 'twitter.views.add_twitter_acct'),
    url(r'^sayhello', 'twitter.views.tweeter'),
    url(r'^newIssueAll/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_all_new_issue'),
)