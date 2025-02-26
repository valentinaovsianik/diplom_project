from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView

from users.permissions import IsAdmin, IsStudent, IsTeacher

from .models import Answer, Course, Lesson, Question, Test, TestResult
from .serializers import (
    AnswerSerializer,
    CourseSerializer,
    LessonSerializer,
    QuestionSerializer,
    TestResultSerializer,
    TestSerializer,
)
from .services import calculate_score


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


class TestCreateApiView(CreateAPIView):
    """Создание теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAdmin | IsTeacher,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TestListApiView(ListAPIView):
    """Список тестов"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class TestRetrieveApiView(RetrieveAPIView):
    """Получение информации о тесте"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class TestUpdateApiView(UpdateAPIView):
    """Обновление теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class TestDestroyApiView(DestroyAPIView):
    """Удаление теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class TestSubmitApiView(CreateAPIView):
    """Предствление для выполнения теста"""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = (IsStudent,)

    def perform_create(self, serializer):
        test = serializer.validated_data["test"]
        answers = serializer.validated_data["answers"]

        # Рассчитываем баллы с помощью функции calculate_score
        score = calculate_score(test, answers)

        # Сохраняем результат теста
        serializer.save(student=self.request.user, score=score)


# Представления для Question
class QuestionListApiView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class QuestionRetrieveApiView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class QuestionCreateApiView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class QuestionUpdateApiView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class QuestionDestroyApiView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdmin | IsTeacher,)


# Представления для Answer
class AnswerListApiView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class AnswerRetrieveApiView(RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class AnswerCreateApiView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class AnswerUpdateApiView(UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdmin | IsTeacher,)


class AnswerDestroyApiView(DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAdmin | IsTeacher,)
