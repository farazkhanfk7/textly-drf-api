from django.contrib.auth.models import User
from .models import Text
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    staff_of = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

    
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['sentence']