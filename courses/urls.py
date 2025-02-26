from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import (
    CourseCreateApiView, CourseListApiView, CourseRetrieveApiView, CourseUpdateApiView, CourseDestroyApiView,
    LessonCreateApiView, LessonListApiView, LessonRetrieveApiView, LessonUpdateApiView, LessonDestroyApiView
)


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
]

urlpatterns += router.urls

