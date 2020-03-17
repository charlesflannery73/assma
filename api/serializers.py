from rest_framework import serializers

from web.models import Org


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = '__all__'
