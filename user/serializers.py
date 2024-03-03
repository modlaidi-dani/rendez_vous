from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User,Group
class UserSerialier(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, allow_blank=False)
    last_name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False, min_length=8, write_only=True)
    class Meta:
        model=User
        fields=('first_name','last_name','email','password')
    def create(self, validated_data):
        validated_data['username'] = validated_data.get('email')
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
class SerializerUpdatePassword(serializers.Serializer):
    old_password = serializers.CharField(required=True, allow_blank=False, min_length=8, write_only=True)
    new_password = serializers.CharField(required=True, allow_blank=False, min_length=8, write_only=True)
    new_password_conf = serializers.CharField(required=True, allow_blank=False, min_length=8, write_only=True)
    
    def validate(self,data):
        if not data.get('new_password') or not data.get('new_password_conf'):
            raise serializers.ValidationError('Please write your old password and password confirmation')
        if data.get('new_password')!=data.get('new_password_conf'):
            raise serializers.ValidationError('Confirmation password is note the samme as password')
        return data
class ForgetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['email']
