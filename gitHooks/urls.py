from django.conf.urls import patterns


urlpatterns = patterns('gitHooks.views',
    (r'^$', 'index'),
    (r'push$', 'hookPush'),
)
