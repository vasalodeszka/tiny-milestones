from rest_framework import serializers

from apps.children.models import Child


class ChildrenSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Child
        fields = "__all__"
        read_only_fields = ["id"]
