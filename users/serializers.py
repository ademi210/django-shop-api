from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
    confirm_password = serializers.CharField(min_length=6)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('пароль не совпадает')
        return data

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь с таким username уже существует.")
        return username


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class SMSCodeSerializer(serializers.Serializer):
    sms_code = serializers.CharField(max_length=6)