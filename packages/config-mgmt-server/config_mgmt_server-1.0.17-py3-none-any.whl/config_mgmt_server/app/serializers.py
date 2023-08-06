
from rest_framework import serializers
from .models import ISOFile
 
class ISOFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISOFile
        fields = ('name', 'data')