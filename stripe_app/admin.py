from django.contrib import admin

from users.forms import User
from .models import *
from modules.utils import *


@admin.register(StripeCustomer)
class StripeCustomer(admin.ModelAdmin):
    list_display = ['user', 'customer_id', 'email', 'phone', '_user_type', 'currency', 'created_at', 'updated_at', ]
    list_per_page = 50
    search_fields = ["user__username", "customer_id", "email", "phone"]
    readonly_fields = ['_user_type', 'user', 'customer_id', 'name','email', 'phone', 'currency', 'customer_api_details']
    exclude = ['user_type']

    def _user_type(self, obj: User) -> str:
        if obj.user_type == 2:
            return 'Customer'
        elif obj.user_type == 3:
            return 'Driver'
        else:
            return 'Unknown'
    
    _user_type.short_description = 'User Type'

    def customer_api_details(self, instance):
        api_details = instance.api_details()
        if api_details:
            return json_style_prettify(api_details)
        return None

    customer_api_details.short_description = 'Customer Details'


@admin.register(CustomerPaymentSource)
class CustomerPaymentSourceAdmin(admin.ModelAdmin):
    list_display = ['source_id', 'customer', 'is_default', 'created_at', 'updated_at']
    readonly_fields = ['source_id', 'customer', 'is_default', 'fingerprint', 'get_details', ]
    list_per_page = 50
    search_fields = ["source_id", "customer__customer_id"]

    def get_fields(self, request, obj=None):
        fields = super(self.__class__, self).get_fields(request, obj)
        fields_list = list(fields)
        fields_list.remove('details')
        fields_tuple = tuple(fields_list)
        return fields_tuple

    def get_details(self, instance):
        if instance.details:
            return json_style_prettify(instance.details)
        return None

    get_details.short_description = 'Details'