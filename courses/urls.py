from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (AnswerCreateApiView, AnswerDestroyApiView, AnswerListApiView, AnswerRetrieveApiView,
                    AnswerUpdateApiView, CourseCreateApiView, CourseDestroyApiView, CourseListApiView,
                    CourseRetrieveApiView, CourseUpdateApiView, LessonCreateApiView, LessonDestroyApiView,
                    LessonListApiView, LessonRetrieveApiView, LessonUpdateApiView, QuestionCreateApiView,
                    QuestionDestroyApiView, QuestionListApiView, QuestionRetrieveApiView, QuestionUpdateApiView,
                    TestCreateApiView, TestDestroyApiView, TestListApiView, TestRetrieveApiView, TestSubmitApiView,
                    TestUpdateApiView)

app_name = "courses"

router = SimpleRouter()

urlpatterns = [
    # Маршруты для курсов
    path("", CourseListApiView.as_view(), name="course-list"),
    path("create/", CourseCreateApiView.as_view(), name="course-create"),
    path("<int:pk>/", CourseRetrieveApiView.as_view(), name="course-detail"),
    path("<int:pk>/update/", CourseUpdateApiView.as_view(), name="course-update"),
    path("<int:pk>/delete/", CourseDestroyApiView.as_view(), name="course-delete"),
    # Маршруты для уроков
    path("lessons/", LessonListApiView.as_view(), name="lesson-list"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson-create"),
    path("lessons/<int:pk>/", LessonRetrieveApiView.as_view(), name="lesson-detail"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson-update"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson-delete"),
    # Маршруты для тестов
    path("tests/", TestListApiView.as_view(), name="test-list"),
    path("tests/create/", TestCreateApiView.as_view(), name="test-create"),
    path("tests/<int:pk>/", TestRetrieveApiView.as_view(), name="test-detail"),
    path("tests/<int:pk>/update/", TestUpdateApiView.as_view(), name="test-update"),
    path("tests/<int:pk>/delete/", TestDestroyApiView.as_view(), name="test-delete"),
    path("tests/<int:pk>/submit/", TestSubmitApiView.as_view(), name="test-submit"),
    # Маршруты для Question
    path("questions/", QuestionListApiView.as_view(), name="question-list"),
    path("questions/create/", QuestionCreateApiView.as_view(), name="question-create"),
    path("questions/<int:pk>/", QuestionRetrieveApiView.as_view(), name="question-detail"),
    path("questions/<int:pk>/update/", QuestionUpdateApiView.as_view(), name="question-update"),
    path("questions/<int:pk>/delete/", QuestionDestroyApiView.as_view(), name="question-delete"),
    # Маршруты для Answer
    path("answers/", AnswerListApiView.as_view(), name="answer-list"),
    path("answers/create/", AnswerCreateApiView.as_view(), name="answer-create"),
    path("answers/<int:pk>/", AnswerRetrieveApiView.as_view(), name="answer-detail"),
    path("answers/<int:pk>/update/", AnswerUpdateApiView.as_view(), name="answer-update"),
    path("answers/<int:pk>/delete/", AnswerDestroyApiView.as_view(), name="answer-delete"),
]

urlpatterns += router.urls
