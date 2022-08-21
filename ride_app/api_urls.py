from django.urls import path, include

urlpatterns = [
    path("api/v1/", include('ride_app.api.v1.urls', namespace='api_v1')),
]
