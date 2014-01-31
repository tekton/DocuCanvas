from django.conf import settings
# mail
from django.core.mail import EmailMessage  #, send_mail
from django.template import Context
from django.template.loader import get_template
# /mail
from issues.models import SubscriptionToIssue, Issue, IssueComment

import datetime
import celery

"""
    Goals: use a mail queue that each mail is created in

    Using a queue system with every mail seperate allows for far more custimization to cater to everyones needs.
    This also allows for things like message headers to be different, and priority queues on communication- send to assigned when critial is changed, but everyone elses update just gets to when its gotten to.
"""

def prepMailingList(issue, update_type="update"):
    '''
        Create new redis set(?) for e-mail list
        A set should limit the e-mail addresses being prepped!
    '''
    mail_to = set()
    subs = None
    # get people that are subscribed to the issue
    try:
        print issue.id
        subs = SubscriptionToIssue.objects.filter(issue=issue.id)
    except Exception as e:
        print "Unable to find subscriptions..."
        print e
        # should do more, but it's alpha...
    if subs is not None:
        for sub in subs:
            mail_to.add(sub.user.email)
    # get people assigned to the issue
    try:
        assigned_to = issue.assigned_to.email
    except:  # we don't care about why it didn't work really...
        assigned_to = None
    if assigned_to is not None:
        mail_to.add(assigned_to)
    # get people that have mail settings set to all updates
    if update_type == "created":
        '''
            this is a special situation where we need to mail the creator of the item
        '''
        mail_to.add(issue.created_by.email) 
    return mail_to


def prepTweetList():
    pass


def prepFacebookList():
    pass


def prepBodyOfMail(issue, update_type="update", comment=False):
    '''
        Depending on the nature of the communication the body will change very slightly

        todo: add validation
    '''
    # if update...
    # if created...
    # if assigned?
    rtn_dict = {}
    rtn_dict["update_type"] = update_type
    rtn_dict["issue"] = issue
    rtn_dict["timestamp"] = datetime.datetime.now()
    rtn_dict["url_base"] = settings.URL_BASE
    rtn_dict["project_name"] = issue.project.name
    rtn_dict["site_title"] = settings.INSTALL_NAME
    if comment:
        rtn_dict["comment"] = comment.description
        rtn_dict["comment_user"] = comment.user
    return rtn_dict


def prepSubjectOfMail(issue, update_type="update", item="Issue"):
    '''
        Depending on the nature of the communication the subject will change very slightly
    '''
    ### TODO add try to make sure issue actually exists
    try:
        Issue.objects.get(pd=issue.id)
    except Exception as e:
        print "Item doesn't exist yet...oh well, prep mail anyway!"
        print e
    #
    if update_type == "update":
        msg = "Updated"
    elif update_type == "created":
        msg = "Created"
    elif update_type == "assigned":
        msg = "Assigned To You"
    elif update_type == "comment":
        msg = "Has A New Comment"
    else:
        msg = "Had Something Happen That You Should Know About ... also SYNTAX ERROR"
    # if update...
    ## [<install name>] Issue <id> Updated
    # if created...
    ## [<install name>] New Issue Created <ID>
    # if assigned?
    ## [<install name>] Issue <ID> Assigned To You
    rtn_str = "[{0}] {1} {2} {3}".format(settings.INSTALL_NAME, item, issue.id, msg)
    print rtn_str
    return rtn_str

#TODO - convert to celery task
@celery.task
def prepMail(issue, update_type='update', comment=False):
    '''
        Called from the issue save function

        Sends an issue object- not just the ID

        Options for update
            update
            created
            assigned ## should really be re-evaled later?
            help  ## should move to own section...
            comment - type of update
    '''
    # get mail ID
    subject = prepSubjectOfMail(issue, update_type)
    body = prepBodyOfMail(issue, update_type, comment)
    mail_to = prepMailingList(issue, update_type)
    html_content = get_template('email/index-inline.html').render(Context(body))
    mail_from = settings.EMAIL_SENDER
    msg = EmailMessage(subject, html_content, mail_from, mail_to)
    msg.content_subtype = "html"  # Main content is now text/html; needs to be called after context is set
    try:
        print "Attempting to send message"
        msg.send()
    except Exception as e:
        print "Unable to send mail"
        print e
        print mail_to, mail_from, subject
