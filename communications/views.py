# Create your views here.
from django.conf import settings
# mail
from django.core.mail import send_mail, EmailMessage
from django.template import Context
from django.template.loader import get_template
# /mail

def prepMailingList(issue, update_type="update"):
    '''
        Create new redis set(?) for e-mail list
        A set should limit the e-mail addresses being prepped!
    '''
    # get people that are subscribed to the issue
    # get people assigned to the issue
    # get people that have mail settings set to all updates
    if update_type == "created":
        '''
            this is a special situation where we need to mail the creator of the item
        '''
        pass 
    pass


def prepTweetList():
    pass


def prepFacebookList():
    pass


def prepBodyOfMail(issue, update_type="update"):
    '''
        Depending on the nature of the communication the body will change very slightly
    '''
    # if update...
    # if created...
    # if assigned?
    pass


def prepSubjectOfMail(issue, update_type="update", item="Issue"):
    '''
        Depending on the nature of the communication the subject will change very slightly
    '''
    ### TODO add try to make sure issue actually exists
    try:
        Issue.objects.get(pd=issue.id)
    except Exception as e:
        print e
        return False
    #
    if update_type == "update":
        msg = "Updated"
    elif update_type == "created":
        msg = "Created"
    elif update_type == "assigned":
        msg = "Assigned To You"
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


def prepMail(issue, update_type='update'):
    '''
        Called from the issue save function

        Options for update
            update
            created
            assigned ## should really be re-evaled later?
            help  ## should move to own section...
    '''
    # get mail ID
    subject = prepSubjectOfMail(issue, update_type)
    prepBodyOfMail(issue, update_type)
    prepMailingList(issue, update_type)
    pass


def sendMail(mail_id):
    # get all the things from redis....
    mailing_list = True  ## get from redis based on mail_id
    # old code...
    subject = 'New Issue Creted :: {0}'.format(issue.id)
    html_content = get_template('email/index.html').render(
                Context({
                    'username': request.user,
                    'issue': issue,
                })
              )
    mmail = settings.EMAIL_SENDER
    
    msg = EmailMessage(subject, html_content, mmail, [mmail])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
