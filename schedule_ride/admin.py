from django.contrib import admin
from .models import *


@admin.register(ScheduleRide)
class ScheduleRide(admin.ModelAdmin):
    list_display = ['customer', 'driver', 'day', 'date', 'start_time', 'end_at', 'total_hours', 'total_price', '_canceled_by']
    list_per_page = 50
    search_fields = ["day", "date", "start_time", "total_hours", "total_price"]
    readonly_fields = ['customer','driver','day','date','start_time','end_at','total_hours','total_price','pick_up_location','pick_up_latitude', 'pick_up_longitude', 'drop_off_location', 
                       'drop_off_longitude','drop_off_latitude','is_canceled','_canceled_by','is_active','created_at','updated_at']
    exclude = ['canceled_by']

    def has_change_permission(self, request, obj=None):
        return False

    def _canceled_by(self, obj) -> str:
        if obj.canceled_by == '2':
            return 'Customer'
        elif obj.canceled_by == '3':
            return 'Driver'
        else:
            return 'Null'
