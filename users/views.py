from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Q, Sum
from django.http import Http404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .serializers import UserRegisterSerializer, UserProfileSerializer, UserPasswordChangeSerializer, UsersListSerializer
from .models import EducationCentre
from students.models import Student


class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    http_method_names=['post']

    def post(self,request,*args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.pop('password2')
        password=data.pop('password1')
        user_data = {
            **data,
            "password": password
        }# more info about using args and kwargs : https://stackoverflow.com/questions/11315010/what-do-and-before-a-variable-name-mean-in-a-function-signature
        user = EducationCentre.objects.create_user(**user_data)
        serializer = UserProfileSerializer(user)
        data = {'user': serializer.data, 'is_admin': user.is_superuser}
        return Response(data, status=status.HTTP_201_CREATED)


class ChangePasswordView(APIView):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)

    def post(self,request, *args, **kwargs):
        serializer = UserPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = get_object_or_404(EducationCentre, ECemail=email)
        password = request.data['new_password']
        user.set_password(password)
        user.save()
        return Response({"message":"Password has been changed successfully"}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
     queryset = EducationCentre.objects.all()
     serializer_class = UserProfileSerializer
     permission_classes = (IsAuthenticated,)

     def patch(self, request, *args, **kwargs):
         user = self.get_object()
         serializer = UserProfileSerializer(instance=user, data=request.data, partial=True)
         serializer.is_valid(raise_exception=True)
         serializer.save()
         return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserStatisticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self,pk):
        try:
            user = EducationCentre.objects.get(id=pk)
        except user.DoesNotExist:
            raise Http404

    def get(self,request,pk, *args,**kwargs):
        user = self.get_object(id=pk)
        students = Student.objects.filter(only_contacted__education_centre=user)
        today = date.today()
        expected_money = 0
        result_money = 0
        for student in students:
            paid_fee = student.has_paid_fee
            date_for_last_payment = student.date_for_last_payment
            total_payment_per_month = student.total_payment_per_month
            loan = student.total_loan_amount

            num_of_months_for_loan = (today.year - date_for_last_payment.year) * 12 + (
                        today.month - date_for_last_payment.month) - 1
            penalty_amount = 0
            for obj in student.penalty.all():
                penalty_amount += obj.penalty_in_percent
            total_payment_of_month = 0
            for obj in student.penalty.all():
                total_payment_of_month += obj.cost_per_month
            loan_amount = loan + num_of_months_for_loan * total_payment_per_month + penalty_amount * total_payment_per_month / 100
            total_payment_of_cmonth = total_payment_per_month + penalty_amount * total_payment_per_month / 100
            expected_money+=total_payment_of_cmonth
            if paid_fee == True and num_of_months_for_loan == -1:
                result_money += total_payment_of_cmonth
                student.total_payment_per_month=0
                student.save(update_fields=['total_payment_per_month'])
            if paid_fee == True and num_of_months_for_loan == 0:
                student.has_paid_fee=False
                student.total_payment_per_month=total_payment_of_cmonth
                student.save(update_fields=['total_payment_per_month', 'has_paid_fee'])
            if paid_fee == False and num_of_months_for_loan > 0:
                student.total_loan_amount=loan_amount
                student.total_payment_per_month=total_payment_of_month
                student.save(update_fields=['total_payment_per_month', 'total_loan_amount'])
            if paid_fee == True and num_of_months_for_loan > 0:
                student.has_paid_fee=False
                student.total_payment_per_month=total_payment_of_month
                student.total_loan_amount=loan_amount
                student.save(update_fields=['has_paid_fee', 'total_payment_per_month', 'total_loan_amount'])

        data = {
            'expected_money' : expected_money,
            'result_money' : result_money,

        }

        return Response(data, status=status.HTTP_200_OK)

class UserListView(APIView):
    permission_classes=(IsAdminUser,)
    pagination_class  = LimitOffsetPagination

    def get(self,request,*args,**kwargs):
        search = request.query_params.get('search')
        users = EducationCentre.objects.all()
        if search:
            search_list = str(search).split(' ')
            queries = [Q(ECemail__icontains=word) |
                       Q(ECphonenumber__icontains=word) |
                       Q(ECname__icontains=word) for word in search_list]
            query = queries.pop()
            for items in queries:
                query |= items
            users = users.filter(query)

        serializer = UsersListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # If a `data=` argument is passed (it must be passed like this: Serializer(data=blu or blu.blu) then:
    # serializer.is_valid() - Available.
    # serializer.initial_data - Available.
    # serializer.validated_data - Only available after calling `is_valid()=True`
    # serializer.errors - Only available after calling `is_valid()`
    # serializer.data - Only available after calling `is_valid()`
    #   If a `data=` argument is not passed (it must be passed like this: Serializer(data=blu or blu.blu)then:
    #   serializer.is_valid() - Not available.
    #   serializer.initial_data - not available.
    #   serializer.validated_data - Not available.
    #   serializer.errors - Not available.
    #   serializer.data - Available.

    # serializer.initial_data - we can use it before validation(is_valid=True)
    # serializer.data - we can use it after validation with not validated values
    # we can not directly use request.user, instead if we use concrete views we should call self.get_object() in user related model,
    # else we have to get it like this(EducationCentre.objects.get(email=email))
    # request.data - incoming data from frontend part in json format
    # serializer.validated_data - we can use ut after validation with validated values
    # serializer converts incoming data in json format to python native data type. This process is called deserializing
    # serializer converts complex data(queryset, object..) to python native data type(dict,..). This is called serializing.
    # Python native data type is converted to json in Response
    # is_valid is called in create(), update(), partial_update(). Because other actions dont take incoming data
    # More info about request-response cycle in the url: https://sourcery.blog/how-request-response-cycle-works-in-django-rest-framework/
    # data : is a dict and you can see it only after is_valid() (you can see only not validated values)
    # validated_data is an OrderedDict and you can see it only after is_valid() and is_valid() == True









