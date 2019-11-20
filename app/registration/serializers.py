from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ValidationCode
from django.contrib.auth.hashers import make_password


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class RegistrationValidationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'username')
        read_only_fields = ('id',)

    # def required(value):
    #     if value is None:
    #         raise serializers.ValidationError('This field is required')

    # https://stackoverflow.com/questions/55906891
    # without this django stores the provided password as plaintext
    def validate_password(self, value: str) -> str:  # -> is an annotation
        return make_password(value)


class ValidationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidationCode
        fields = ('id', 'user', 'code', 'status')
        read_only_fields = ('id',)
