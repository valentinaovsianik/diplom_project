from rest_framework import serializers

from .models import Answer, Course, Lesson, Question, Test, TestResult


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса"""

    owner = serializers.EmailField(source="owner.email", read_only=True)  # Показываем только email владельца

    class Meta:
        model = Course
        fields = "__all__"

    def create(self, validated_data):
        """Автоматически назначаем владельца"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["owner"] = request.user  # Устанавливаем текущего пользователя
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор урока"""

    owner = serializers.EmailField(source="owner.email", read_only=True)  # Показываем только email владельца
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())  # Передаем ID курса

    class Meta:
        model = Lesson
        fields = "__all__"

    def create(self, validated_data):
        """Автоматически назначаем владельца"""
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["owner"] = request.user  # Устанавливаем текущего пользователя
        return super().create(validated_data)


from rest_framework import serializers


class TestSerializer(serializers.ModelSerializer):
    """Сериализатор теста"""

    class Meta:
        model = Test
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор ответа"""

    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор вопроса"""

    answers = AnswerSerializer(many=True, read_only=True)  # Вложенный сериализатор для ответов

    class Meta:
        model = Question
        fields = "__all__"


class TestResultSerializer(serializers.ModelSerializer):
    """Сериализатор результата теста"""

    class Meta:
        model = TestResult
        fields = "__all__"
