from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register('card', viewsets.CustomerPaymentSourceAPIView, basename='stripe_card')

app_name = 'stripe_app'

urlpatterns = [
    path('config/', viewsets.StripeConfiguration.as_view()),
    path('my-customer-account/', viewsets.MyCystomerAccount.as_view()),
    path('', include(router.urls)),
]