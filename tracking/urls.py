from django.urls import path,include
from rest_framework import routers
from tracking import views

router = routers.DefaultRouter()
router.register('tracking', views.TrackingModelViewSet,basename='tracking')
router.register('requests', views.RequestModelViewSet,basename='request')

urlpatterns = [
    path('', include(router.urls)),
    path('accept-request/',views.AcceptRequestAPI.as_view()),
    path('end-request/',views.EndRequestAPI.as_view()),
]