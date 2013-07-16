try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url
from haystack.views import SearchView
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().filter(author='john')

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(), name='haystack_search'),
)
