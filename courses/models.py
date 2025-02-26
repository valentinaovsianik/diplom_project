from django.db import models
from users.models import User

class Course(models.Model):
    """Модель курса"""
    name = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", verbose_name="Владелец курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
    def __str__(self):
        return self.name

class Lesson(models.Model):
    """Модель урока"""
    title = models.CharField(max_length=255, verbose_name="Название урока")
    content = models.TextField(verbose_name="Содержание урока")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lessons", verbose_name="Владелец урока")
    image = models.ImageField(
        upload_to="lessons/", verbose_name="Изображение урока", blank=True, null=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
