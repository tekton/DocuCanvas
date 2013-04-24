from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'DocuCanvas.views.home', name='home'),
    # url(r'^DocuCanvas/', include('DocuCanvas.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^$', 'dashboard.views.home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('auth.urls')),
    #
    url(r'^bug/', include('bugs.urls')),
    url(r'^board/', include('boards.urls')),
    #url(r'^suggestion/', include('suggestions.urls')),
    #url(r'^task/', include('tasks.urls')),
    #url(r'^node/', include('nodes.urls')),
    url(r'^checklist/', include('checklists.urls')),
    url(r'^project/', include('projects.urls')),
    url(r'^issue/', include('issues.urls')),
    url(r'^reports/', include('daily_reports.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'^food/', include('food.urls')),
    url(r'^help/', include('helpdesk.urls')),
    url(r'^gapps/', include('gapps.urls')),
)
