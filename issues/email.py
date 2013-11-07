import celery
from models import Issue, SubscriptionToIssue

@celery.task
def prepAndSendEmail(issue_id):
    issue = Issue.objects.get(pk=issue_id)
    subscribers = SubscriptionToIssue.objects.filter(issue=issue_id)
    email_list = {}
    for subscriber in subscribers:
        try:
            email_list[subscriber.user.id] = subscriber.user.email
        except Exception as e:
            print e
            # send mail to the admin that the user doesn't have an e-mail...but is "subscribed" or "assigned"
    email_list[issue.assigned_to.id] = issue.assigned_to.email
