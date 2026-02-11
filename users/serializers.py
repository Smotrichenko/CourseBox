from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания платежа"""

    class Meta:
        model = Payment
        fields = ("paid_course", "paid_lesson", "amount", "payment_method")

        def validate(self, attrs):
            paid_course = attrs.get("paid_course")
            paid_lesson = attrs.get("paid_lesson")

            if not paid_course and not paid_lesson:
                raise serializers.ValidationError("Нужно указать курс или урок.")
            if paid_course and paid_lesson:
                raise serializers.ValidationError(
                    "Нельзя одновременно выбирать и курс, и урок."
                )

            return attrs


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода платежа"""

    class Meta:
        model = Payment
        fields = "__all__"
