from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.kids.models import Kid
from apps.kids.serializers import KidSerializer


class KidViewSet(ModelViewSet):
    serializer_class = KidSerializer
    permission_classes = [IsAuthenticated]
    model = Kid

    def get_queryset(self):
        return Kid.objects.filter(created_by=self.request.user)
