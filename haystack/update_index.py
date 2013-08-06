from haystack.management.commands import update_index
import celery


@celery.task
def update_index(video):
try:
    update_index.Command().handle()
except Exception, e:
    print 'unable to update index'
    print e