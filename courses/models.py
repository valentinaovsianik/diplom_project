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
    image = models.ImageField(upload_to="lessons/", verbose_name="Изображение урока", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Test(models.Model):
    """Модель теста"""

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tests", verbose_name="Урок")
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание теста")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tests", verbose_name="Владелец теста")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель вопроса"""

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions", verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text


class Answer(models.Model):
    """Модель ответа"""

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    text = models.CharField(max_length=255, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class TestResult(models.Model):
    """Модель результата теста"""

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="results", verbose_name="Тест")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results", verbose_name="Студент")
    score = models.IntegerField(verbose_name="Баллы")
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выполнения")

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"

    def __str__(self):
        return f"{self.student.email} - {self.test.title}"
