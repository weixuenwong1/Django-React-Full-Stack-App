from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # represents the user
        fields = ["id", "username", "password"]  # fields that we want to serialise when accepting a new user and when returning a new user
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # create user after receiving validated data
        return user 
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note  # represens the Note object
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}