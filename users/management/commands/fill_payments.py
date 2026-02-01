from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()

        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Нет пользователей в базе."))
            return

        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not course and not lesson:
            self.stdout.write(self.style.ERROR("Нет ни курсов, ни уроков."))
            return

        Payment.objects.create(
            user=user,
            paid_lesson=lesson,
            amount=300,
            payment_method=Payment.PAYMENT_METHOD_CASH
        )

        self.stdout.write(self.style.SUCCESS("Платежи успешно добавлены."))
