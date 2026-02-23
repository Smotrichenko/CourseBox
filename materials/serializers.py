from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_only_youtube_links


class LessonSerializer(serializers.ModelSerializer):

    description = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[validate_only_youtube_links],
    )
    video_url = serializers.URLField(validators=[validate_only_youtube_links])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    description = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
        validators=[validate_only_youtube_links],
    )

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        requests = self.context.get("request")
        if not requests or not requests.user.is_authenticated:
            return False
        return Subscription.objects.filter(user=requests.user, course=obj).exists()
