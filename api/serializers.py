from rest_framework import serializers

from web.models import Org, Asset


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = '__all__'


class AssetDetailSerializer(serializers.ModelSerializer):
    org = OrgSerializer()

    class Meta:
        model = Asset
        fields = '__all__'
