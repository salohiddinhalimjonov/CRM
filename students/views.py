from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student, AttendedMockLesson
from .serializers import TimeUnitSerializer, AdvertisementSerializer, TeacherSerializer, CourseSerializer,\
    OnlyContactedSerializer, StudentSerializer,AttendedMockLessonSerializer



class TimeUnitView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def get(self,request,*args,**kwargs):
        time_unit = TimeUnit.objects.filter(education_centre=request.user)
        serializer = TimeUnitSerializer(time_unit, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        serializer = TimeUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(education_centre=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TimeUnitViewPK(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def patch(self,request,*args,**kwargs):
        serializer = TimeUnitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(education_centre=request.user)


class AdvertisementViewSet(ModelViewSet):
    permission_classes=(IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        advertisement = Advertisement.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self,serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self,serializer):
        serializer.save(education_centre=self.request.user)

    def get(self,request,*args,**kwargs):
        search = request.query_params.get('search')
        advertisement = self.get_queryset()
        if search is not None:
            advertisement = advertisement.filter(name__icontains=search)
        serializer = AdvertisementSerializer(advertisement, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)   


class CourseView():
    pass