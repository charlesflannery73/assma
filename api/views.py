from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q

from web.models import Org, Asset
from .serializers import OrgSerializer, AssetSerializer


class OrgViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given match.
    list:
    Return a list of all the existing matches.
    create:
    Create a new match instance.
    """
    queryset = Org.objects.all()
    serializer_class = OrgSerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer













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