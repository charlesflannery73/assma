from django.contrib import admin
from .models import Org, Asset, Sector, Level, AssetType

admin.site.register(Sector)
admin.site.register(Level)
admin.site.register(Org)
admin.site.register(Asset)
admin.site.register(AssetType)
