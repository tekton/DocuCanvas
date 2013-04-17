from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="img", height_field='height', width_field='width')
#    image = models.CharField(max_length=255)  # image URI
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class BoardNote(models.Model):
    board = models.ForeignKey(Board)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.title


class BoardNode(models.Model):
    board = models.ForeignKey(Board)
    nodeLink = models.IntegerField(null=True, blank=True)
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    nodeType = models.CharField(max_length=255, null=True, blank=True, default='note')

    #nodeLink = models.IntegerField(null=True, blank=True)  # Basic foreign key to nodeType
    # Fields used for testing
    #user = models.ForeignKey(User)
    #title = models.CharField(max_length=255)
    #description = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.id)

