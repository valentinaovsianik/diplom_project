from rest_framework.generics import (
    CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
)
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsAdmin, IsTeacher, IsStudent


class CourseCreateApiView(CreateAPIView):
    """Создание курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher,)

    def perform_create(self, serializer):
        """Определение владельца курса"""
        serializer.save(owner=self.request.user)


class CourseListApiView(ListAPIView):
    """Список всех курсов"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class CourseRetrieveApiView(RetrieveAPIView):
    """Получение информации о конкретном курсе"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class CourseUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном курсе"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class CourseDestroyApiView(DestroyAPIView):
    """Удаление конкретного курса"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdmin | IsTeacher,)

    def perform_create(self, serializer):
        """Определение владельца урока"""
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Список всех уроков"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class LessonRetrieveApiView(RetrieveAPIView):
    """Получение информации о конкретном уроке"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class LessonUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном уроке"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class LessonDestroyApiView(DestroyAPIView):
    """Удаление конкретного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAdmin | IsTeacher,)
