from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.children.models import Child
from apps.children.serializers import ChildrenSerializer


class ChildrenViewSet(ModelViewSet):
    serializer_class = ChildrenSerializer
    permission_classes = [IsAuthenticated]
    model = Child

    def get_queryset(self):
        return Child.objects.filter(created_by=self.request.user)
