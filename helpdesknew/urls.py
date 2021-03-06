from django.conf.urls import *

urlpatterns = patterns('',
    (r'^new$', 'helpdesknew.views.help_form'),
    # (r'^error_page/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.error_page'),
    (r'^pending$', 'helpdesknew.views.get_pending'),
    (r'^resolved$', 'helpdesknew.views.get_resolved'),
    (r'^acknowledge/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.ack_answer'),
    (r'^cmmtedit/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.edit_comment'),
    (r'^edit/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.edit_question'),
    (r'^close_question_91990/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.close_question'),
    (r'^response/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.submit_response'),
    (r'^$', 'helpdesknew.views.user_help'),
    (r'^user$', 'helpdesknew.views.user_help'),
    (r'^mark_the_answer/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.mark_the_answer'),
    (r'^mark_the_input/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.mark_the_input'),
    (r'^suggestion/([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.mark_suggestion'),
    (r'^([A-Za-z0-9_\.-]+)$', 'helpdesknew.views.get_help'),
)
