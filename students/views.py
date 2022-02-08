from datetime import date
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q,Sum
from rest_framework import status, generics, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import TimeUnit, Advertisement, Teacher, Course, OnlyContacted, Student,Penalty
from .serializers import TimeUnitSerializer, AdvertisementSerializer, TeacherSerializer, CourseSerializer,\
    OnlyContactedSerializer, StudentSerializer, PenaltySerializer, StudentListSerializer


class TimeUnitView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = TimeUnitSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        advertisement = TimeUnit.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self,serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self,serializer):
        serializer.save(education_centre=self.request.user)

    @action(detail=False, methods=['GET'])
    def desc_ordered(self,request,*args,**kwargs):
        time_unit = self.get_queryset()
        time_unit = time_unit.order_by('-name')
        serializer = TimeUnitSerializer(time_unit, many=True)
        return Response(serializer.data)


class AdvertisementViewSet(ModelViewSet):
    permission_classes=(IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    search_fields = ['name']

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

    def retreive(self,request,*args,**kwargs):
        student = self.get_object()
        paid_fee = student.has_paid_fee
        date_for_last_payment = student.date_for_last_payment
        total_payment_per_month = student.total_payment_per_month
        loan = student.total_loan_amount
        today = date.today()

        num_of_months_for_loan = (today.year - date_for_last_payment.year) * 12 + (today.month - date_for_last_payment.month) - 1
        penalty_amount = student.penalty.aggregate(Sum('penalty_in_percent')).get('penalty_in_percent__sum')
        total_payment_of_month = student.courses.aggregate(Sum('cost_per_month')).get('cost_per_month__sum')
        loan_amount = loan + num_of_months_for_loan * total_payment_per_month + penalty_amount * total_payment_per_month / 100

        if paid_fee == True and num_of_months_for_loan == -1:
            student.update(total_payment_per_month=0)
        if paid_fee==True and num_of_months_for_loan==0:
            total_payment_of_month = total_payment_per_month + penalty_amount * total_payment_per_month / 100
            student.update(paid_fee=False,total_payment_per_month=total_payment_of_month)
        if paid_fee==False and num_of_months_for_loan > 0:
            student.update(total_loan_amount=loan_amount, total_payment_per_month=total_payment_of_month)
        if paid_fee == True and num_of_months_for_loan > 0:
            student.update(has_paid_fee=False,total_payment_per_month=total_payment_of_month, total_loan_amount=loan_amount)

        serializer = StudentSerializer(data=student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,*args,**kwargs):
        student=self.get_object()
        if student.total_loan_amount > 0:
            return Response({'message':'Student has a loan. This method is not allowed!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            student.delete()
            return Response({'message':'Student ro\'yhatdan o\'chirildi'}, status=status.HTTP_204_NO_CONTENT)


class StudentViewListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()

    def get_serializer_class(self):
        if self.request.method=='GET':
            return StudentListSerializer
        return StudentSerializer

    def get(self,request,*args,**kwargs):
        selected_course_id = request.query_params.get('course_id', None)
        penalty = request.query_params.get('penalty',None)
        search = request.query_params.get('search',None)
        not_paid_fee = request.query_params.get('paid_fee',None)
        if selected_course_id:
            queryset = self.queryset.filter(selected_course=selected_course_id)
        if penalty:
            queryset = queryset.filter(penalty=penalty)
        if not_paid_fee:
            queryset = queryset.filter(has_paid_fee=False)
        if search:
            search_list = str(search).split(' ')
            queries = [Q(student_id__icontains=word) |
                       Q(parent_phone_number__icontains=word) for word in search_list]
            query = queries.pop()
            for items in queries:
                query |= items
            queryset = queryset.filter(query)
        serializer = StudentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = AdvertisementSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['experience', 'full_name']
    filterset_fields = ['course']

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
        course_id = request.query_params.get('course')
        if course_id:
            teachers = teachers.filter(courses=course_id)
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
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['cost_per_month', 'name']
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        course = Course.objects.filter(education_centre=user)
        return course

    def perform_create(self, serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self, serializer):
        serializer.save(education_centre=self.request.user)

    @action(detail=True,method=['POST'], url_path='add-student')
    def add_student(self,request,pk, *args,**kwargs):
        course = self.get_object()
        student_id = request.data['student_id']
        student = Student.objects.get(pk=student_id)
        student.selected_course.add(course)
        student.save()
        return Response({'status':'Success!'})

    @action(detail=True,method=['POST'], url_path='add-teacher')
    def add_teacher(self,request,pk,*args,**kwargs):
        course = self.get_object()
        teacher_id = request.data['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.course.add(course)
        teacher.save()
        return Response({'status':'Success!'})

    @action(detail=True,method=['POST'], url_path='remove-student')
    def remove_student(self,request,pk,*args,**kwargs):
        course = self.get_object()
        student_id = request.data['student_id']
        student=Student.objects.get(pk=student_id)
        student.course.remove(course)
        student.save()
        return Response({'status':'Success!'})

    @action(detail=True, method=['POST'], url_path='remove-teacher')
    def remove_teacher(self, request, pk, *args, **kwargs):
        course = self.get_object()
        teacher_id = request.data['teacher_id']
        teacher = Teacher.objects.get(pk=teacher_id)
        teacher.course.remove(course)
        teacher.save()
        return Response({'status': 'Success!'})


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
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


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
    serializer_class = OnlyContactedSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['full_name']
    search_fields = ['full_name', 'phone_number']
    filterset_fields = ['advertisement', 'has_been_student']

    def get_queryset(self):
        user = self.request.user
        advertisement = Advertisement.objects.filter(education_centre=user)
        return advertisement

    def perform_create(self, serializer):
        serializer.save(education_centre=self.request.user)

    def perform_update(self, serializer):
        serializer.save(education_centre=self.request.user)