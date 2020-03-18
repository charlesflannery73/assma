from rest_framework import serializers

from web.models import Org, Asset


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    #org = serializers.SlugRelatedField(read_only=True, slug_field='name')
    org = serializers.StringRelatedField()
    #org = serializers.CharField(read_only=True,source='org.name')
    #org = OrgSerializer()

    class Meta:
        model = Asset
        #fields = '__all__'
        fields = ['id', 'name', 'org', 'org_id', 'type', 'comment', 'created', 'modified']

    # def to_representation(self, instance):
    #     org = super(AssetSerializer, self).to_representation(instance)
    #     org['org_id'] = instance.org.id
    #     return org

class AssetDetailSerializer(serializers.ModelSerializer):
    org = OrgSerializer()

    class Meta:
        model = Asset
        fields = '__all__'
        #fields = ['id', 'name', 'org', 'org_id', 'type', 'comment', 'created', 'modified']
