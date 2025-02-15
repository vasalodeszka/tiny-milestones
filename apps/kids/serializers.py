from rest_framework import serializers

from apps.kids.models import Kid


class KidSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Kid
        fields = "__all__"
        read_only_fields = ["id"]
