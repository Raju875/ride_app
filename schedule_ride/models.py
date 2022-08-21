from django.utils.translation import ugettext_lazy as _
from django.db import models
from users.models import CustomerProfile,DriverProfile,UserType

from availability.models import DAY_CHOICES


class ScheduleRide(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='schedule_request_customer')
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,related_name='schedule_request_driver')
    day = models.CharField(choices=DAY_CHOICES.Choices, max_length=25, null=True, default=None)
    date = models.DateField()
    start_time = models.TimeField()
    end_at = models.DateTimeField(null=True)
    total_hours = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=7, decimal_places=3, null=True, default=None)
    pick_up_location = models.CharField(max_length=255)
    pick_up_latitude = models.CharField(max_length=50)
    pick_up_longitude = models.CharField(max_length=50)
    drop_off_location = models.CharField(max_length=255)
    drop_off_longitude = models.CharField(max_length=50)
    drop_off_latitude = models.CharField(max_length=50)
    is_canceled = models.BooleanField(default=False)
    canceled_by = models.CharField(max_length=100,choices=UserType.Choices,null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.customer.email + " | " + self.drop_off_location

    class Meta:
        verbose_name = _('Schedule Ride')
        verbose_name_plural = _("Schedule Rides")
        ordering = ['-id']
