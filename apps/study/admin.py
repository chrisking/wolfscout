##### Global Imports #####
from django.contrib import admin

##### Local Imports #####
from apps.study.models import Study

##### Admin Classes ######
class StudyAdmin(admin.ModelAdmin):
    list_display = ('owner',)
    search_fields = ('owner',)


##### Admin Registers ######
admin.site.register(Study, StudyAdmin)