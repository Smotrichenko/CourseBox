from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings

from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id: int) -> dict:
    """Асихронная рассылка писем подписчикам курса"""

    course = Course.objects.filter(id=course_id).first()
    if not course:
        return {"status": "course_not_found"}

    subs = Subscription.objects.filter(course=course).select_related("user")

    emails = [s.user.email for s in subs if s.user.email]
    if not emails:
        return {"status": "no_subscribers"}

    send_mail(
        subject=f"CourseBox: обновление курса '{course.title}'.",
        message="Материалы курса были обновлены.",
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=emails,
        fail_silently=False,
    )

    return {"status": "sent", "count": len(emails)}



