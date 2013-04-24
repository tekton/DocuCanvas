from django.contrib import admin
from models import *

'''
class CheckListLayoutItemsInline(admin.TabularInline):
    model = CheckListLayoutItems


class ChecklistTagInline(admin.TabularInline):
	model = ChecklistTag


class ChecklistAdmin(admin.ModelAdmin):
	inlines = [CheckListLayoutItemsInline]


class ChecklistInstanceAdmin(admin.ModelAdmin):
	inlines = [ChecklistTagInline]
'''

class createUserAdmin(admin.ModelAdmin):
	exclude = ('admin_pass',)
	
admin.site.register(createUser, createUserAdmin)
