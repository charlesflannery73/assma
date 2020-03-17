from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from web.models import Org
from .serializers import OrgSerializer

@api_view(['GET', 'POST'])
def org_list(request):

    if request.method == "GET":
        orgs = Org.objects.all()
        serializer = OrgSerializer(orgs, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = OrgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def org_detail(request, pk):

    try:
        org = Org.objects.get(pk=pk)
    except Org.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = OrgSerializer(org)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = OrgSerializer(org, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        org.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)