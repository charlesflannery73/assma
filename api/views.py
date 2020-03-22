from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from web.models import Org, Asset
from .serializers import OrgSerializer, AssetSerializer, AssetDetailSerializer


class OrgViewSet(viewsets.ModelViewSet):
    """
    list:
    filter parameters: name, name_like, id, level, tier, comment

    create:
    add create help here

    read:
    add read help here

    update:
    add update help here

    partial_update:
    add partial update help here

    delete:
    add delete help here
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Org.objects.all()
    serializer_class = OrgSerializer

    def get_queryset(self):

        queryset = Org.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        name_like = self.request.query_params.get('name_like', None)
        if name_like is not None:
            queryset = queryset.filter(name__contains=name_like)

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        level = self.request.query_params.get('level', None)
        if level is not None:
            queryset = queryset.filter(level=level)

        tier = self.request.query_params.get('tier', None)
        if tier is not None:
            queryset = queryset.filter(tier=tier)

        comment = self.request.query_params.get('comment', None)
        if comment is not None:
            queryset = queryset.filter(comment__contains=comment)

        return queryset

class AssetViewSet(viewsets.ModelViewSet):
    """
    list:
    filter parameters: name, name_like, id, org_id, org, org_like, type, comment

    create:
    add create help here

    read:
    add read help here

    update:
    add update help here

    partial_update:
    add partial update help here

    delete:
    add delete help here
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    detail_serializer_class = AssetDetailSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class
        return super().get_serializer_class()

    def get_queryset(self):

        queryset = Asset.objects.all()

        org_like = self.request.query_params.get('org_like', None)
        if org_like is not None:
            queryset = queryset.filter(org__name__contains=org_like)

        org = self.request.query_params.get('org', None)
        if org is not None:
            queryset = queryset.filter(org__name=org)

        org_id = self.request.query_params.get('org_id', None)
        if org_id is not None:
            queryset = queryset.filter(org_id=org_id)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        name_like = self.request.query_params.get('name_like', None)
        if name_like is not None:
            queryset = queryset.filter(name__contains=name_like)

        id = self.request.query_params.get('id', None)
        if id is not None:
            queryset = queryset.filter(id=id)

        type = self.request.query_params.get('type', None)
        if type is not None:
            queryset = queryset.filter(type=type)

        comment = self.request.query_params.get('comment', None)
        if comment is not None:
            queryset = queryset.filter(comment__contains=comment)

        return queryset
