from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "apps.children"

router = SimpleRouter()
router.register(r"children", views.ChildrenViewSet, basename="children")

urlpatterns = [path("api/v1/", include(router.urls))]
