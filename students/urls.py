from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TimeUnitViewSet,AdvertisementViewSet,StudentView,StudentViewListCreate,PenaltyView,\
    PenaltyViewListCreate,TeacherViewSet,CourseViewSet,OnlyContactedViewSet

router = DefaultRouter()
router.register('advertisement', AdvertisementViewSet, basename='advertisement')
router.register('time_unit', TimeUnitViewSet, basename='time_unit')
router.register('teacher', TeacherViewSet, basename='teacher')
router.register('course', CourseViewSet, basename='course')
router.register('only_contacted',OnlyContactedViewSet, basename='only_contacted')

urlpatterns = [
    path('', include(router.urls)),
    path('student/', StudentViewListCreate.as_view(), name='student'),
    path('student/<int:pk>/', StudentView.as_view(), name='student_detail'),
    path('penalty/', PenaltyViewListCreate.as_view(), name='penalty'),
    path('penalty/<int:pk>/', PenaltyView.as_view(), name='penalty_detail')
]





















