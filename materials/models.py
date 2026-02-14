from django.conf import settings
from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses",
    )

    title = models.CharField(max_length=300)
    preview = models.ImageField(
        upload_to="materials/course_previews/", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="lessons",
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")

    title = models.CharField(max_length=300)
    preview = models.ImageField(
        upload_to="materials/lesson_previews/", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(max_length=500)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "materials.Course", on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return f"{self.user} -> {self.course}"
