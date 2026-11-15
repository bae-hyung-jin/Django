from django.contrib import admin
from walkmap.models import AccidentSpot


@admin.register(AccidentSpot)
class AccidentSpotAdmin(admin.ModelAdmin):
    list_display = ('year', 'gu_name', 'spot_nm', 'occrrnc_cnt', 'caslt_cnt', 'dth_dnv_cnt', 'lat', 'lng')
    list_filter = ('year', 'gu_name')
    search_fields = ('spot_nm', 'spot_cd')

