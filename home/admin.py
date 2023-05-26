from django.contrib import admin
import admin_thumbnails
from mptt.admin import DraggableMPTTAdmin
from .models import Setting, BillCode

admin.site.register(Setting)
admin.site.register(BillCode)
