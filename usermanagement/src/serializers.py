from rest_framework import serializers
from .models import UserManagement

class GetUserByIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)

class CreateManagementSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, min_length=3, max_length=100)
    last_name = serializers.CharField(required=True, min_length=3, max_length=100)
    username = serializers.CharField(required=True, min_length=3, max_length=20)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True, min_length=10, max_length=15)
    
    def bind(self, validated_data):
        return UserManagement(**validated_data)

class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1, min_value=1, max_value=500)
    limit = serializers.IntegerField(required=False, default=10, min_value=1, max_value=500)

class ManagementSerializer(serializers.Serializer):
    def single_representation(self, instance):
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "username": instance.username,
            "email": instance.email,
            "phone": instance.phone,
            "is_active": instance.is_active
        }

    def response(self, instance):
        arr = []
        for i in instance:
            arr.append(self.single_representation(i))
        return arr


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=3, max_length=20)
    password = serializers.CharField(required=True, min_length=8, max_length=20)
    first_name = serializers.CharField(required=True, min_length=3, max_length=100)
    last_name = serializers.CharField(required=True, min_length=3, max_length=100)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True, min_length=10, max_length=15)
    
    def bind(self, validated_data):
        return UserManagement(**validated_data)
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=3, max_length=20)
    password = serializers.CharField(required=True, min_length=8, max_length=20)
        
    def bind(self, validated_data):
        return UserManagement(**validated_data)
    

class ChangePasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=3, max_length=20)
    old_password = serializers.CharField(required=True, min_length=8, max_length=20)
    new_password = serializers.CharField(required=True, min_length=8, max_length=20)
    

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, min_length=3, max_length=20)
    email = serializers.EmailField(required=True)