from rest_framework import serializers

from .models import User


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("uuid", "username", "email", "first_name", "last_name", "is_active")
