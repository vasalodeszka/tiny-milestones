from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

router = SimpleRouter()
router.register(r"users", views.UserRetrieveViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/blacklist/", views.CustomTokenBlacklistView.as_view(), name="token_blacklist"),
    path("api/v1/token/refresh/", views.CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
