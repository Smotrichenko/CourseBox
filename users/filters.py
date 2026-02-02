import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            "paid_course": ["exact"],
            "paid_lesson": ["exact"],
            "payment_method": ["exact"],
        }
