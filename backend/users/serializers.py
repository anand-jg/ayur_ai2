from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, UserHealthProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 
                 'first_name', 'last_name', 'phone_number']
        extra_kwargs = {
            'phone_number': {'required': False, 'allow_blank': True},
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = '__all__'
        read_only_fields = ('user', 'rating', 'total_ratings')

class UserHealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserHealthProfile
        fields = '__all__'
        read_only_fields = ('user',)
