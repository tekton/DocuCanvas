from django.contrib import admin
from models import *


class createUserAdmin(admin.ModelAdmin):
    exclude = ('admin_pass',)

admin.site.register(createUser, createUserAdmin)
