from django.urls import path
from .views import UserRegisterView, UserProfileView, ChangePasswordView,UserStatisticsView, UserListView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register-view'),
    path('change_password/', ChangePasswordView.as_view(), name='change-password'),
    path('user_list/',UserListView.as_view(), name='users' ),
    path('user_statistics/',UserStatisticsView.as_view(), name='users-statistics' ),
    path('<int:pk>/', UserProfileView.as_view(), name='profile-view')
]
