from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import MaterialsPagination
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    pagination_class = MaterialsPagination
    queryset = Course.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="moderators").exists():
            qs = qs.filter(owner=self.request.user)
        return qs.order_by("id")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["create"]:
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ["destroy"]:
            self.permission_classes = [IsAuthenticated, IsOwner & ~IsModerator]

        return [permission() for permission in self.permission_classes]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination
    queryset = Lesson.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name="moderators").exists():
            qs = qs.filter(owner=self.request.user)
        return qs.order_by("id")


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner & ~IsModerator]


class SubscriptionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        user = request.user

        course = get_object_or_404(Course, pk=course_id)

        subs_qs = Subscription.objects.filter(user=user, course=course)

        if subs_qs.exists():
            subs_qs.delete()
            message = "Подписка удалена."
        else:
            Subscription.objects.filter(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
