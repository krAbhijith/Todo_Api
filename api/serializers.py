from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from api.models import Todo

from django.contrib.auth.models import User


class TodoSerializers(ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class RegisterSerializer(Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('username is already taken')
            
        if data['email']:
            if User.objects.filter(email = data['email']).exists():
                raise serializers.ValidationError('Email is already taken')
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class LoginSerializer(Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
