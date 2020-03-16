from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q

from web.models import Org, Sector, Level

class OrgSerializer(serializers.ModelSerializer):
    sector = serializers.SlugRelatedField(read_only=True, slug_field='sector')
    sector_id = serializers.IntegerField(write_only=True)
    level = serializers.SlugRelatedField(read_only=True, slug_field='level')
    level_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Org
        #fields = ['id', 'name', 'sector', 'sector_id', 'level', 'level_id', 'tier', 'comment', 'created', 'modified']
        fields = '__all__'
