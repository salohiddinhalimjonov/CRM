from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student,Penalty
from .serializers import TimeUnitSerializer, AdvertisementSerializer, TeacherSerializer, CourseSerializer,\
    OnlyContactedSerializer, StudentSerializer, PenaltySerializer


class TimeUnitView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = TimeUnitSerializer

    def get_queryset(self):
        user = self.request.user
        advertisement = TimeUnit.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self,serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self,serializer):
        serializer.save(education_centre=self.request.user)


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
        search = request.query_params.get('search')#please, provide search in this format: ?search="bla-bla-bla"
        advertisement = self.get_queryset()
        if search is not None:
            advertisement = advertisement.filter(name__icontains=search)
        serializer = AdvertisementSerializer(advertisement, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self,request,*args,**kwargs):
        pass


class StudentViewListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    def get(self,request,*args,**kwargs):
        pass


class TeacherView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        advertisement = Advertisement.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self, serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self, serializer):
        serializer.save(education_centre=self.request.user)


    def get(self,request,*args, **kwargs):
        search = request.query_params.get('search')
        teachers = self.get_queryset()
        category_id = request.query_params.get('category')
        if category_id:
            teachers = teachers.filter(courses=category_id)
        if search:
            search_list = str(search).split(' ')
            queries = [Q(full_name__icontains=word) |
                       Q(passport_id__icontains=word) for word in search_list]
            query = queries.pop()
            for items in queries:
                query |= items
            teachers = teachers.filter(query)
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseView(ModelViewSet):
    pass


class PenaltyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        penalty = Penalty.objects.filter(education_centre=user)
        return penalty

    def patch(self,request,*args,**kwargs):
        obj = self.get_object()
        serializer = PenaltySerializer(instance=obj, data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save(education_centre=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PenaltyViewListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PenaltySerializer
    def get_queryset(self):
        user = self.request.user
        penalty = Penalty.objects.filter(education_centre=user)
        return penalty

    def perform_create(self,serializer):
        serializer.save(education_centre=self.request.user)


class OnlyContacted(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = AdvertisementSerializer

    def get_queryset(self):
        user = self.request.user
        advertisement = Advertisement.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self, serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self, serializer):
        serializer.save(education_centre=self.request.user)