from rest_framework import serializers
from .models import Users,Blog
from argon2 import PasswordHasher

ph = PasswordHasher()
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ['username','email','password']

    def create(self, validated_data):
        validated_data['password'] = ph.hash(validated_data['password'])
        return super().create(validated_data)

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id','title', 'content', 'slug', 'author']

    def create(self, validated_data):
        return super().create(validated_data)