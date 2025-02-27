from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from users.permissions import IsAdmin, IsStudent, IsTeacher

from .models import Answer, Course, Lesson, Question, Test, TestResult
from .serializers import (AnswerSerializer, CourseSerializer, LessonSerializer, QuestionSerializer,
                          TestResultSerializer, TestSerializer)


@method_decorator(name="create", decorator=swagger_auto_schema(operation_description="Создание нового курса"))
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
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class CourseRetrieveApiView(RetrieveAPIView):
    """Получение информации о конкретном курсе"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdmin | IsTeacher | IsStudent,)


class CourseUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном курсе"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class CourseDestroyApiView(DestroyAPIView):
    """Удаление конкретного курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )

    def perform_create(self, serializer):
        """Определение владельца урока"""
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Список всех уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class LessonRetrieveApiView(RetrieveAPIView):
    """Получение информации о конкретном уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class LessonUpdateApiView(UpdateAPIView):
    """Изменение информации о конкретном уроке"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class LessonDestroyApiView(DestroyAPIView):
    """Удаление конкретного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class TestCreateApiView(CreateAPIView):
    """Создание теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TestListApiView(ListAPIView):
    """Список тестов"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class TestRetrieveApiView(RetrieveAPIView):
    """Получение информации о тесте"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class TestUpdateApiView(UpdateAPIView):
    """Обновление теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class TestDestroyApiView(DestroyAPIView):
    """Удаление теста"""

    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class TestSubmitApiView(CreateAPIView):
    """Представление для выполнения теста"""

    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = (
        IsAuthenticated,
        IsStudent,
    )

    def perform_create(self, serializer):
        test = serializer.validated_data["test"]
        answers = serializer.validated_data["answers"]

        def calculate_score(test, answers):
            """Расчет баллов для теста"""
            score = 0
            for question in test.questions.all():
                # Получаем список ID правильных ответов для текущего вопроса
                correct_answers = question.answers.filter(is_correct=True).values_list("id", flat=True)

                # Получаем список ID ответов пользователя для текущего вопроса
                user_answers = answers.get(str(question.id), [])

                # Сравниваем ответы пользователя с правильными ответами
                if set(user_answers) == set(correct_answers):
                    score += 1
            return score

        score = calculate_score(test, answers)  # Вычисляем баллы

        # Сохраняем результат теста
        serializer.save(student=self.request.user, score=score)


# Представления для Question
class QuestionListApiView(ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class QuestionRetrieveApiView(RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class QuestionCreateApiView(CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class QuestionUpdateApiView(UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class QuestionDestroyApiView(DestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


# Представления для Answer
class AnswerListApiView(ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class AnswerRetrieveApiView(RetrieveAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher | IsStudent,
    )


class AnswerCreateApiView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class AnswerUpdateApiView(UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )


class AnswerDestroyApiView(DestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (
        IsAuthenticated,
        IsAdmin | IsTeacher,
    )
