from dateutil.relativedelta import relativedelta
from django.utils import timezone

from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def block_inactive_users() -> dict:
    """Если пользователь не заходил больше месяца - ставим is_active=False """

    month_ago = timezone.now() - relativedelta(months=1)

    qs = User.objects.filter(is_active=True, last_login__isnull=False, last_login__lt=month_ago)

    updated = qs.update(is_active=False)

    return {"status": "ok", "blocked": updated}
