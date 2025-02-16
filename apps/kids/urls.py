from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "apps.kids"

router = SimpleRouter()
router.register(r"kids", views.KidViewSet, basename="kids")

urlpatterns = [path("api/v1/", include(router.urls))]
