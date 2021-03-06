##### Global Imports #####
from django.contrib.gis import admin

from apps.crawler.gpscollar.models import Collar, CollarData

##### Admin Classes ######

class CollarAdmin(admin.GeoModelAdmin):
    list_display = ('collarID',)
    search_fields = ('collarID',)

class CollarDataAdmin(admin.GeoModelAdmin):
    list_display = ('collar','LMT_DATETIME','LATITUDE','LONGITUDE',)
    search_fields = ('collar','LMT_DATETIME','LATITUDE','LONGITUDE',)


##### Admin Registers ######
admin.site.register(Collar, CollarAdmin)
admin.site.register(CollarData, CollarDataAdmin)