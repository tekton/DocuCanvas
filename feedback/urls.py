from django.conf.urls import *

urlpatterns = patterns('',
	(r'^feedback$', 'feedback.views.feedback'),
	(r'^submit_feedback$', 'feedback.views.submit_feedback'),
    (r'^anonymous$', 'feedback.views.all_anonymous'),
    (r'^signed$', 'feedback.views.all_signed'),
    (r'^anonymous/([A-Za-z0-9_\.-]+)$', 'feedback.views.anonymous_view'),
    (r'^signed/([A-Za-z0-9_\.-]+)$', 'feedback.views.signed_view'),
)