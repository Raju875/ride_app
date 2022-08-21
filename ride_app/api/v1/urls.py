from django.urls import path, include

app_name = 'api_v1'

urlpatterns = [
    path('', include('home.api.v1.urls')),
    path("profile/", include("users.api.v1.urls", namespace="profile")),
    path("", include("availability.api.v1.urls", namespace="availability")),
    path("", include("schedule_ride.api.v1.urls", namespace="schedule_ride")),
    path("", include("tracking.urls")),
    path("stripe/", include("stripe_app.api.v1.urls")),
]
