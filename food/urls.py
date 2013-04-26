from django.conf.urls import *

urlpatterns = patterns('',
    (r'new', 'food.views.food_form'),
    (r'overview', 'food.views.food_overview'),
    (r'comp/([A-Za-z0-9_\.-]+)', 'food.views.food_received'),
    (r'view/([A-Za-z0-9_\.-]+)', 'food.views.user_food_overview'),
    (r'all', 'food.views.all_food'),
    (r'complete', 'food.views.food_overview_complete'),
    (r'([A-Za-z0-9_\.-]+)', 'food.views.get_food'),
)
