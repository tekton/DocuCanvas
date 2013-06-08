from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

from newsfeed.models import NewsFeedItem
# Create your models here.


class FoodRequest(models.Model):
    quantity_choices = (
        ('lbs', 'Pounds'),
        ('qty', 'Items'),
        ('ltr', 'Litres'),
        ('gal', 'Gallons'),
    )
    user = models.ForeignKey(User)  # name of user making request
    item = models.CharField(max_length=255)  # item being requested
    quantity = models.FloatField(default=0)  # amount of item being requested
    quantity_type = models.CharField(max_length=3, choices=quantity_choices, default=(1, 1))  # type of quantity ex. lbs, ltr, gal
    request_initiated = models.DateField(auto_now_add=True, null=True, blank=True)  # when request was initated
    desired_completion = models.DateTimeField(blank=True, null=True)  # when user wants request completed
    request_completed_bool = models.NullBooleanField(default=False)  # bool for whether or not request has been completed
    request_completed_date = models.DateField(auto_now=True, blank=True, null=True)  # date request was handled
    cost_per_quantity = models.FloatField(default=0)  # cost per unit of item requested
    total_cost = models.FloatField(default=0)  # total cost of order (per unit price * # of units)

    def __unicode__(self):
        return self.user.username + ':' + self.item

    def FindTotal(self):
        self.total_cost = self.quantity * self.cost_per_quantity

admin.site.register(FoodRequest)
