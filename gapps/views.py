from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from forms import *
import gdata.apps.client
import gdata.apps.groups.client
import gdata.apps.emailsettings.client

# Create your views here.

def create_user(request):
	userForm = createUser()
	if request.method == 'POST':
		form = UserForm(request.POST, instance=userForm)
		userForm = form.save()
		admin_user = userForm.admin_user
		admin_pass = userForm.admin_pass

		first_name = userForm.first_name
		last_name = userForm.last_name
		email_address = userForm.email_address
		temp_pass = userForm.temp_pass
		job_title = userForm.job_title
		extension = userForm.extension
		mobile_number = userForm.mobile_number
		add_to_groups = userForm.add_to_groups.split(', ')
		newEmail = email_address + "@domain_goes_here"
		

		phoneLine = '<font size = "1" face = "sans-serif">Mobile: ' + mobile_number + '</font><br />'

		# Excludes the line with mobile number if one is not entered
		if mobile_number == "":
			phoneLine = ""
			
		# create connection to change simple email settings
		emailClient = gdata.apps.emailsettings.client.EmailSettingsClient(domain='domain_goes_here')
		emailClient.ClientLogin(email=admin_user, password=admin_pass, source='apps')
		emailClient.ssl = True

		# create connection to change group settings
		groupClient = gdata.apps.groups.client.GroupsProvisioningClient(domain='domain_goes_here')
		groupClient.ClientLogin(email=admin_user, password=admin_pass, source='apps')
		groupClient.ssl = True

		# create connection for creating a new client
		client = gdata.apps.client.AppsClient(domain='domain_goes_here')
		client.ClientLogin(email=admin_user, password=admin_pass, source='apps')
		client.ssl = True

		# create new user
		client.CreateUser(email_address, last_name, first_name, temp_pass)
		# create nickname using first name of user
		client.CreateNickname(email_address, first_name)

		# add user to groups
		for i in add_to_groups:
			groupClient.AddMemberToGroup(i, newemail)
		groupClient.AddMemberToGroup('default_group', newEmail)

		emailClient.UpdateSignature(username=email_address, signature=	'<img src = "signature_image_goes_here" /><br />' + 
				                                    '<font size = "1" face = "sans-serif">' + first_name + " " + last_name + '</font><br />' +
				                                    '<font size = "1" face = "sans-serif">' + job_title + '</font></strong><br />' +
				                                    '<font size = "1" face = "sans-serif">Phone:  phone_number - Ext: ' + extension + ' </font><br />' + phoneLine +
				                                    '<font size = "1" face = "sans-serif"><a href = "mailto:' + newEmail + '">' + newEmail + '</a></font><br />' +
				                                    '<font size = "1" face = "sans-serif"><a href = "domain_goes_here">domain_goes_here</a></font><br />' +
				                                    '<strong><font size = "1" face = "sans-serif">stuff_goes_here</font></strong>')

		
		print admin_user
		print admin_pass
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
		form = UserForm()

	return render_to_response('gapps/create_user.html', {'form': form}, context_instance=RequestContext(request))
