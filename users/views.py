from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer, UserPasswordChangeSerializer, UsersListSerializer
from .models import EducationCentre

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
         return Response(serializer.data)


class UserListView(APIView):
    permission_classes=(IsAdminUser,)

    def get(self,request,*args,**kwargs):#add some features
        users = EducationCentre.objects.all()
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









