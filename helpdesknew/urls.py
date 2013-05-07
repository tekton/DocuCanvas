from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'new', 'helpdesknew.views.help_form'),
    (r'error_page/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.error_page'),
    #(r'all', 'helpdesknew.views.get_all'),
    (r'pending', 'helpdesknew.views.get_pending'),
    (r'resolved', 'helpdesknew.views.get_resolved'),
    (r'close_question_9919/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.close_question'),
    (r'response/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.submit_response'),
    (r'mark/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.mark_as_answer'),
    (r'user/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.user_help'),
    (r'dontlookhere/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.bypass_user'),
    (r'mark_the_answer/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.mark_the_answer'),
    (r'mark_the_input/([A-Za-z0-9_\.-]+)', 'helpdesknew.views.mark_the_input'),
    (r'([A-Za-z0-9_\.-]+)', 'helpdesknew.views.get_help'),
)
