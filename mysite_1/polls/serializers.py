from rest_framework import serializers
from polls.models import *
from django.contrib.auth.models import User

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ('id', 'name', 'platform', 'date', 'genre', 'rating', 'info')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        data = super(UserSerializer, self).validate(attrs)
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password mismatch')
        del data['password2']
        return data

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, user, validated_data):
        user.username = validated_data['username']
        user.set_password(validated_data['password'])
        user.save()
        return user