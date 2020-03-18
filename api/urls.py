from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from .views import OrgViewSet, AssetViewSet


router = DefaultRouter()
router.register('v1/org', OrgViewSet, 'api_org_list')
router.register('v1/asset', AssetViewSet, 'api_asset_list')
schema_view = get_schema_view(title='Assma API',
                              description='An API to query orgs or assets',
                              version=1
                              )


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema/', schema_view),
    path('api/docs/', include_docs_urls(title='Assma API')),
]
