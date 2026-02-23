from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import (
    PaymentSerializer,
    UserRegisterSerializer,
    UserSerializer,
    PaymentCreateSerializer,
)
from users.services import (
    stripe_create_product,
    stripe_create_price,
    stripe_create_checkout_session,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserRegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        self.payment = serializer.save(user=self.request.user)

        if self.payment.paid_course:
            name = self.payment.paid_course.title
            description = self.payment.paid_course.description or ""
        else:
            name = self.payment.paid_lesson.title
            description = self.payment.paid_lesson.description or ""

        product_data = stripe_create_product(name=name, description=description)

        price_data = stripe_create_price(
            product_id=product_data["id"],
            amount=self.payment.amount * 100,
            currency="rub",
        )

        session_data = stripe_create_checkout_session(price_id=price_data["id"])

        self.payment.strip_product_id = product_data["id"]
        self.payment.strip_price_id = price_data["id"]
        self.payment.strip_session_id = session_data["id"]
        self.payment.payment_url = session_data.get("url")
        self.payment.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(PaymentSerializer(self.payment).data)
