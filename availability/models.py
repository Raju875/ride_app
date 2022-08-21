from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()
from users.models import DriverProfile


class DAY_CHOICES:
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'

    Choices = (
        (Monday, Monday),
        (Tuesday, Tuesday),
        (Wednesday, Wednesday),
        (Thursday, Thursday),
        (Friday, Friday),
        (Saturday, Saturday),
        (Sunday, Sunday),
    )


class Availability(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver_availability')
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='driver_availability', null=True)
    day = models.CharField(_('Day'), choices=DAY_CHOICES.Choices, default=DAY_CHOICES.Monday,  max_length=25)
    date = models.DateField(_('Date'), null=True, default=None)
    whole_day = models.BooleanField(default=False)
    start_time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.user

    class Meta:
        verbose_name = _('Driver Availability')
        verbose_name_plural = _("Driver Availabilies")
        ordering = ['-id']
