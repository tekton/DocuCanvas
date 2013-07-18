from django.conf.urls import *

urlpatterns = patterns('',
    (r'^anonymous/new$', 'feedback.views.anonymous_feedback'),
    (r'^signed/new$', 'feedback.views.signed_feedback'),
    (r'^anonymous$', 'feedback.views.all_anonymous'),
    (r'^signed$', 'feedback.views.all_signed'),
    (r'^anonymous/([A-Za-z0-9_\.-]+)$', 'feedback.views.anonymous_view'),
    (r'^signed/([A-Za-z0-9_\.-]+)$', 'feedback.views.signed_view'),
)