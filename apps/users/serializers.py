from rest_framework import serializers
from .models import Users
from argon2 import PasswordHasher

ph = PasswordHasher()
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['username','email','password']

    def create(self, validated_data):
        validated_data['password'] = ph.hash(validated_data['password'])
        return super().create(validated_data)