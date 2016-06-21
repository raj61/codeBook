from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = '__all__'
class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
