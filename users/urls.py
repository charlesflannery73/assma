from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views


urlpatterns = [
    path('profile/', user_views.profile, name='profile'),
    path('password/', user_views.change_password, name='change_password'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
