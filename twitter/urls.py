from django.conf.urls import *

urlpatterns = patterns('',
    url(r'^add_account', 'twitter.views.add_twitter_acct'),
    url(r'^rmv_account', 'twitter.views.remove_twitter_acct'),
    url(r'^newComment/([A-Za-z0-9_\.-]+)/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_comment_update'),
    url(r'^newIssue/([A-Za-z0-9_\.-]+)/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_new_issue'),
    url(r'^newIssueAll/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_new_issue_all'),
    url(r'^newProject/([A-Za-z0-9_\.-]+)/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_new_project'),
    url(r'^newProjectAll/([A-Za-z0-9_\.-]+)$', 'twitter.views.send_dm_new_project_all'),
    url(r'^newProjectTweet/([A-Za-z0-9_\.-]+)$', 'twitter.views.new_project_tweet'),
)