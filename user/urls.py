from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('login', views.LoginView.as_view(), name='user_login'),
    path('register', views.UserRegisterView.as_view(), name='user_register'),
    path('admin/login', views.LoginView.as_view(), name='admin_login'),
    path('admin/register', views.AdminRegisterView.as_view(), name='admin_register'),
]