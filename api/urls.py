from api import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from .views import OrgViewSet, AssetViewSet


router = DefaultRouter()
router.register('org', OrgViewSet, 'api_org_list')
router.register('asset', AssetViewSet, 'api_asset_list')
schema_view = get_schema_view(title='Assma API',
                              description='An API to query orgs or assets')


urlpatterns = [
    path('api/', include(router.urls)),
]
