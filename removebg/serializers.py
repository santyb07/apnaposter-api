from rest_framework import serializers
from .models import Person

class PersonSerializaer(serializers.ModelSerializer):
    
    class Meta:
        model = Person
        # fields = ['name','age']
        # exclude = ['name']
        fields = '__all__'

class ImageSerializer(serializers.Serializer):
    image = serializers.ImageField()