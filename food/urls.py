from django.conf.urls import *

urlpatterns = patterns('',
    (r'^new$', 'food.views.submitRequest'),
    (r'overview', 'food.views.food_overview'),
    (r'comp/([A-Za-z0-9_\.-]+)', 'food.views.food_received'),
    (r'view/([A-Za-z0-9_\.-]+)', 'food.views.user_food_overview'),
    (r'^all$', 'food.views.allRequests'),
    (r'^list/all$', 'food.views.viewAllLists'),
    (r'complete', 'food.views.food_overview_complete'),
    (r'list/new', 'food.views.createList'),
    (r'list/(\d+)', 'food.views.viewList'),
    (r'([A-Za-z0-9_\.-]+)', 'food.views.get_food'),
)
