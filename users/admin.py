from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from .models import User, CustomerProfile, CustomerDocuments, DriverProfile, VehicleInfo
from availability.models import Availability
from django.contrib.auth import get_user_model

from users.forms import UserChangeForm, UserCreationForm, CustomerProfileForm, DriverProfileForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = auth_admin.UserAdmin.fieldsets + (("User", {"fields": ("name", "user_type")}),)
    list_display = ["username", "name", "email", "is_superuser", "user_type"]
    list_filter = ["user_type", "is_superuser", "is_staff", "is_active"]
    list_per_page = 25
    search_fields = ["name"]


class CustomerDocumentsInfo(admin.StackedInline):
    model = CustomerDocuments
    exclude = ["user"]


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    inlines = [CustomerDocumentsInfo, ]
    # form = CustomerProfileForm
    list_display = ["full_name", "email", "phone", "is_female",  "is_approved"]
    list_filter = ["is_female", "is_approved", ]
    list_per_page = 25
    search_fields = ["full_name", "email", "phone"]
    exclude = ["is_verify_mail_sent"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user']
        return self.readonly_fields


class VehicleInfo(admin.StackedInline):
    model = VehicleInfo
    exclude = ["user"]


class AvailabilityInfo(admin.StackedInline):
    model = Availability
    extra = 0
    readonly_fields = ['day', 'whole_day', 'start_time', 'end_time']
    exclude = ["is_active"]


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    inlines = [AvailabilityInfo, VehicleInfo]
    # form = DriverProfileForm
    
    list_display = ["full_name", "email", "phone", "is_female",  "is_approved"]
    list_filter = ["is_female", "is_approved", ]
    list_per_page = 25
    search_fields = ["full_name", "email", "phone"]
    exclude = ["is_verify_mail_sent"]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['user']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        try:
            if hasattr(obj, 'vehicle_info'):
                obj.vehicle_info.user = obj.user
                obj.vehicle_info.driver = obj
            super().save_model(request, obj, form, change)
        except Exception as e:
            print(e)
