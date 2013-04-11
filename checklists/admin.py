from django.contrib import admin
from models import *


class CheckListLayoutItemsInline(admin.TabularInline):
    model = CheckListLayoutItems


class ChecklistTagInline(admin.TabularInline):
	model = ChecklistTag


class ChecklistAdmin(admin.ModelAdmin):
	inlines = [CheckListLayoutItemsInline]


class ChecklistInstanceAdmin(admin.ModelAdmin):
	inlines = [ChecklistTagInline]

admin.site.register(Checklist, ChecklistAdmin)
admin.site.register(CheckListLayoutItems)
admin.site.register(ChecklistInstance, ChecklistInstanceAdmin)
admin.site.register(ChecklistTag)