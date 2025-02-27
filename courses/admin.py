from django.contrib import admin

from .models import Answer, Course, Lesson, Question, Test, TestResult


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")
    search_fields = ("name", "owner__email")  # Поиск по названию курса и email владельца
    list_filter = ("owner",)  # Фильтр по владельцу курса


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "owner")
    search_fields = ("title", "course__name", "owner__email")  # Поиск по названию урока и курса и email владельца
    list_filter = ("course",)  # Фильтр по курсу


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "owner")
    list_filter = ("lesson", "owner")
    search_fields = ("title", "owner__email")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "test")
    list_filter = ("test",)
    search_fields = ("text",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("text", "question", "is_correct")
    list_filter = ("question", "is_correct")
    search_fields = ("text",)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("test", "student", "score", "completed_at")
    list_filter = ("test", "student")
    search_fields = ("student__email", "test__title")
