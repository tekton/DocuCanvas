from django.conf.urls.defaults import *

urlpatterns = patterns('', 
	(r'create_user', 'gapps.views.create_user'),
	)