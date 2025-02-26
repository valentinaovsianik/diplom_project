from django.contrib import admin
from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")
    search_fields = ("name", "owner__email") # Поиск по названию курса и email владельца
    list_filter = ("owner",) # Фильтр по владельцу курса


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "course", "owner")
    search_fields = ("title", "course__name", "owner__email") # Поиск по названию урока и курса и email владельца
    list_filter = ("course",) # Фильтр по курсу
