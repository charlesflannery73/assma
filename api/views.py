from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from web.models import Org, Asset
from .serializers import OrgSerializer, AssetSerializer, AssetDetailSerializer, AssetCreateSerializer


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
    queryset = Org.objects.all()
    serializer_class = OrgSerializer

    def create(self, request, *args, **kwargs):
        serializer = OrgSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    detail_serializer_class = AssetDetailSerializer


    def create(self, request, *args, **kwargs):
        serializer = AssetCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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

    # def create(self, request):
    #     message = request.data.pop('message_type')
    #     # check if incoming api request is for new event creation
    #     if message == "NewEvent":
    #         event = request.data.pop('event')
    #         sport = event.pop('sport')
    #         markets = event.pop('markets')[0] # for now we have only one market
    #         selections = markets.pop('selections')
    #         sport = Sport.objects.create(**sport)
    #         markets = Market.objects.create(**markets, sport=sport)
    #         for selection in selections:
    #             markets.selections.create(**selection)
    #         match = Match.objects.create(**event, sport=sport, market=markets)
    #         return Response(status=status.HTTP_201_CREATED)
    #     # check if incoming api request is for updation of odds
    #     elif message == "UpdateOdds":
    #         event = request.data.pop('event')
    #         markets = event.pop('markets')[0]
    #         selections = markets.pop('selections')
    #         for selection in selections:
    #             s = Selection.objects.get(id=selection['id'])
    #             s.odds = selection['odds']
    #             s.save()
    #         match = Match.objects.get(id=event['id'])
    #         return Response(status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)








# @api_view(['GET', 'POST'])
# def org_list(request):
#
#     if request.method == "GET":
#         orgs = Org.objects.all()
#         serializer = OrgSerializer(orgs, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = OrgSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET', 'POST'])
# def asset_list(request):
#
#     if request.method == "GET":
#         assets = Asset.objects.all()
#         serializer = AssetSerializer(assets, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = AssetSerializer(data=request.data)
#         org_val = serializer.data.__getattribute__()
#             request.POST.get('org')
#         print(org_val)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def org_detail(request, pk):
#
#     try:
#         org = Org.objects.get(pk=pk)
#     except Org.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = OrgSerializer(org)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = OrgSerializer(org, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         org.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def asset_detail(request, pk):
#
#     try:
#         asset = Asset.objects.get(pk=pk)
#     except Asset.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == "GET":
#         serializer = AssetSerializer(asset)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = AssetSerializer(asset, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == "DELETE":
#         asset.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)