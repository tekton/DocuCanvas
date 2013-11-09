from django.contrib import admin

from accounts.models import Account
from accounts.views import setAssignable

def make_assignable(modeladmin, request, queryset):
    #print modeladmin
    #print request
    print queryset
    for q in queryset:
        #print q
        print q.id
        setAssignable.delay(q.id)

class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'assignable']
    actions = [make_assignable]

admin.site.register(Account, AccountAdmin)
