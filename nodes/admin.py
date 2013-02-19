from django.contrib import admin

from models import *
from projects.models import *

admin.site.register(Node)
admin.site.register(Project)
admin.site.register(Section)