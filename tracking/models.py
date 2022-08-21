from users.models import CustomerProfile, DriverProfile,UserType
from django.db import models


class Request(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='request_customer')
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE,related_name='request_driver',null=True)
    location = models.CharField(max_length=255,null=True)
    is_accepted = models.BooleanField(default=False)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.customer.email + " | " + self.location


class Tracking(models.Model):
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE)
    driver = models.ForeignKey(DriverProfile,on_delete=models.CASCADE)
    request = models.ForeignKey(Request,on_delete=models.CASCADE,null=True)
    started_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True)
    driver_longitude = models.CharField(max_length=50,null=True)
    driver_latitude = models.CharField(max_length=50,null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    price = models.FloatField(null=True,blank=True)
    ended_by = models.CharField(max_length=100,choices=UserType.Choices,null=True)
    total_distance = models.FloatField(null=True,blank=True)

    def __str__(self) -> str:
        return self.customer.user.email
