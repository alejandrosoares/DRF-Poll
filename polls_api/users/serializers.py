from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username', 'email')

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('user',)

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_fields = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        raw_password = validated_data.get('password')
        new_user = User(username=username, email=email)
        new_user.set_password(raw_password)
        new_user.save()
        return new_user

