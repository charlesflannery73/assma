from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import (
    OrgListView,
    OrgSearch,
    OrgDetailView,
    OrgCreateView,
    OrgUpdateView,
    OrgDeleteView,
    AssetListView,
    AssetDetailView,
    AssetCreateView,
    AssetUpdateView,
    AssetDeleteView,
    AssetSearch,
    HomeView,
)
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='assma-home'),
    path('org/search/', OrgSearch.as_view(), name='org-search'),
    path('org/', OrgListView.as_view(), name='org-list'),
    path('org/<int:pk>/', OrgDetailView.as_view(), name='org-detail'),
    path('org/new/', OrgCreateView.as_view(), name='org-create'),
    path('org/<int:pk>/update/', OrgUpdateView.as_view(), name='org-update'),
    path('org/<int:pk>/delete/', OrgDeleteView.as_view(), name='org-delete'),
    path('asset/', AssetListView.as_view(), name='asset-list'),
    path('asset/search/', AssetSearch.as_view(), name='asset-search'),
    path('asset/<int:pk>/', AssetDetailView.as_view(), name='asset-detail'),
    path('asset/new/', AssetCreateView.as_view(), name='asset-create'),
    path('asset/<int:pk>/update/', AssetUpdateView.as_view(), name='asset-update'),
    path('asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='asset-delete'),
    path('about/', views.about, name='assma-about'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
