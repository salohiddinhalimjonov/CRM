from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeUnitView,AdvertisementViewSet

router = DefaultRouter()
router.register('advertisement', AdvertisementViewSet, basename='advertisement')
urlpatterns = [
    path('time_unit/', TimeUnitView.as_view(), name='time_unit'),
    path('', include(router.urls))
]