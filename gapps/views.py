from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import *
import gdata.apps.client
import gdata.apps.groups.client
import gdata.apps.emailsettings.client


def create_user(request):
    d_bug = False
    userForm = createUser()
    if request.method == 'POST':
        form = UserForm(request.POST, instance=userForm)
        try:
            userForm = form.save()
        except Exception, e:
            print e

        domain_name = userForm.domain_name
        admin_user = userForm.admin_user + "@" + domain_name
        admin_pass = userForm.admin_pass
        #
        first_name = userForm.first_name
        last_name = userForm.last_name
        email_address = userForm.email_address
        temp_pass = userForm.temp_pass
        job_title = userForm.job_title
        extension = userForm.extension
        mobile_number = userForm.mobile_number
        add_to_groups = userForm.add_to_groups
        email_signature = userForm.email_signature
        newEmail = email_address + "@" + domain_name
        # prevent errors if there are no groups to add to
        if add_to_groups != "":
            add_to_groups = userForm.add_to_groups.split(', ')

        # Excludes the line with mobile number if one is not entered
        if mobile_number:
            mobile_number = '<font size = "1" face = "sans-serif">Mobile: ' + mobile_number + '</font><br />'
        else:
            mobile_number = ''

        # prevent errors if there is no email signature
        if email_signature != "":
            email_signature = userForm.email_signature % (first_name, last_name, job_title, extension, mobile_number, newEmail, newEmail)

        # create connection to change simple email settings
        emailClient = gdata.apps.emailsettings.client.EmailSettingsClient(domain=domain_name)
        emailClient.ClientLogin(email=admin_user, password=admin_pass, source='apps')
        emailClient.ssl = True

        # create connection to change group settings
        groupClient = gdata.apps.groups.client.GroupsProvisioningClient(domain=domain_name)
        groupClient.ClientLogin(email=admin_user, password=admin_pass, source='apps')
        groupClient.ssl = True

        # create connection for creating a new client
        client = gdata.apps.client.AppsClient(domain=domain_name)
        client.ClientLogin(email=admin_user, password=admin_pass, source='apps')
        client.ssl = True

        # create new user
        client.CreateUser(email_address, last_name, first_name, temp_pass, change_password='true')

        # add user to groups
        for i in add_to_groups:
            groupClient.AddMemberToGroup(i, newEmail)

        emailClient.UpdateSignature(username=email_address, signature=email_signature)
        if d_bug:
            print admin_user
            print first_name
            print last_name
            print email_address
            print temp_pass
            print job_title
            print extension
            print mobile_number
            print add_to_groups
            for i in add_to_groups:
                print i
        else:
            pass
    else:
        form = UserForm()

    return render_to_response('gapps/create_user.html', {'form': form}, context_instance=RequestContext(request))
