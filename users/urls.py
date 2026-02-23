from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import PaymentListAPIView, UserRegisterAPIView, UserViewSet, PaymentCreateAPIView

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("payments/", PaymentListAPIView.as_view(), name="payments-list"),
    path("", include(router.urls)),
    path("payments/create/", PaymentCreateAPIView.as_view(), name="payment-create"),
]
