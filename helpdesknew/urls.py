from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'new', 'helpdesknew.views.help_form'),
    #(r'all', 'helpdesknew.views.get_all'),
    (r'pending', 'helpdesknew.views.get_pending'),
    (r'resolved', 'helpdesknew.views.get_resolved'),
    (r'response/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.submit_response'),
    (r'mark/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.mark_as_answer'),
    (r'user/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.user_help'),
    (r'dontlookhere/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.bypass_user'),
    (r'([A-Za-z0-9_\.-]+)', 'helpdesknew.views.get_help'),
)
