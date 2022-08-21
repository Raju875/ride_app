from asyncio.windows_events import NULL
from django.core.management import BaseCommand
from datetime import datetime, date
from requests import request
from rest_framework.response import Response
from rest_framework import status

from users.models import CustomerProfile, DriverProfile
from tracking.models import Request, Tracking
from schedule_ride.models import ScheduleRide


class Command(BaseCommand):
    help= "Check every hour and start the schedule ride when time is up"

    def handle(self, *args, **options):
        today = date.today()
        current_time = datetime.now().strftime("%H:%M:%S")
        rides = ScheduleRide.objects.filter(date=today, start_time=current_time, is_active=True, is_canceled=False)
        if not rides:
            print('Not found nay data.')
            return False
        for ride in rides:
            customer = ride.customer
            driver = ride.driver
            request = Request.objects.create(customer=customer,
                                            driver=driver,
                                            location=ride.drop_off_location,
                                            longitude=ride.drop_off_longitude,
                                            latitude=ride.drop_off_latitude,
                                            is_accepted=True)
            Tracking.objects.create(customer=customer,
                                    driver=driver,
                                    driver_longitude=NULL,
                                    driver_latitude=NULL,
                                    request=request)
