from django.db import models


class UserDailyReport(models.Model):
    user = models.IntegerField(default=0)  # would have a lot of things connected to it, like User and other settings
    # TODO change "user" to whatever the full auth item is
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class DailyReport(models.Model):
    # a related pull should get the UserDailyReport list for the date
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    # any other data that should be contained here...
