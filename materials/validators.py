import re
from urllib.parse import urlparse

from rest_framework.serializers import ValidationError

URL_REGEX = re.compile(r"https?://[^\s]+")


def validate_only_youtube_links(value):
    if not value:
        return value

    if value.startswith("http://") or value.startswith("https://"):
        parsed = urlparse(value)
        host = (parsed.netloc or "").lower()

        if host not in ("youtube.com", "www.youtube.com"):
            raise ValidationError("Разрешены ссылки только на youtube.com")
        return value
