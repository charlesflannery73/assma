from django.urls import path
from . import views

urlpatterns = [
    path('org/', views.org_list, name='api_org_list'),
    path('org/<int:pk>/', views.org_detail, name='api_org_detail'),

]
