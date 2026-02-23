from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDAndSubscriptionTests(APITestCase):
    def setUp(self):
        """Тестовые данные"""

        # Группа модераторов
        self.moderators_group, _ = Group.objects.get_or_create(name="moderators")

        # Пользователи
        self.owner_user = User.objects.create_user(
            email="owner@test.com", password="12345"
        )
        self.other_user = User.objects.create_user(
            email="other@test.com", password="12345"
        )
        self.moder_user = User.objects.create_user(
            email="moder@test.com", password="12345"
        )
        self.moder_user.groups.add(self.moderators_group)

        # Курс владельца
        self.course = Course.objects.create(
            title="Course 1", description="Описание без ссылок", owner=self.owner_user
        )

        # Урок владельца
        self.lesson = Lesson.objects.create(
            course=self.course,
            title="Lesson 1",
            description="Описание без ссылок",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            owner=self.owner_user,
        )

    def test_lesson_list_authenticated(self):
        """Список уроков доступен авторизованному пользователю"""

        self.client.force_authenticate(self.owner_user)
        response = self.client.get("/api/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create_owner_allowed(self):
        """Обычный пользователь может создать урок (не модератор)"""

        self.client.force_authenticate(user=self.owner_user)

        data = {
            "course": self.course.id,
            "title": "Lesson 2",
            "description": "Описание",
            "video_url": "https://www.youtube.com/watch?v=aaaa",
        }

        response = self.client.post("/api/lessons/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update_owner_allowed(self):
        """Владелец может редактировать свой урок"""

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.patch(
            f"/api/lessons/{self.lesson.id}/update/", data={"title": "New title"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete_moderator_forbidden(self):
        """Модератор не может удалять уроки"""

        self.client.force_authenticate(user=self.moder_user)

        response = self.client.delete(f"/api/lessons/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_returns_is_subscribed_flag(self):
        """При выборке курса есть признак is_subscribed"""

        self.client.force_authenticate(user=self.owner_user)

        # создаём подписку вручную
        Subscription.objects.create(user=self.owner_user, course=self.course)

        response = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertEqual(response.data["is_subscribed"], True)
