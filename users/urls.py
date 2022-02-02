from django.urls import path
from .views import UserRegisterView, UserProfileView, ChangePasswordView, UserListView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register-view'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('user_list/',UserListView.as_view(), name='users' ),
    path('<int:pk>/', UserProfileView.as_view(), name='profile-view')
]
