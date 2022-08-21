from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register("customer", CustomerProfileViewSet, "customer_profile")
router.register("driver", DriverProfileViewSet, "driver_profile")
# router.register("driver/vehicle/info", VehicleInfoViewSet, "driver_vehicle")
router.register("forgot-password", ForgotPasswordView, basename="forgot_password")
router.register("code-verification", VerificationViewSet, basename="code_verification")
router.register("reset-password", ResetPasswordSetView, basename="reset_password")

app_name = "users"

urlpatterns = [
    path("", include(router.urls)),
]