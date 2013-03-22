from django.db import models

# Create your models here.


class git_commit(models.Model):
    link = models.CharField(max_length=255)
    short_hash = models.CharField(max_length=255)
    long_hash = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    git_user = models.IntegerField(default=0)  # this should really be linked in the secondary auth sections...
    app_user = models.IntegerField(default=0)  # the full auth'd user

    class Meta:
        verbose_name = _('git_commit')
        verbose_name_plural = _('git_commits')

    def __unicode__(self):
        pass
