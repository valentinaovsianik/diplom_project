from rest_framework import serializers
from .models import Course, Lesson
from users.models import User

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
