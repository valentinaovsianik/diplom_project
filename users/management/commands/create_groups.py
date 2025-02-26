from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson

class Command(BaseCommand):
    "Создание групп пользователей и назначение им прав"

    def handle(self, *args, **kwargs):
        # Создаём или получаем группы
        admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        student_group, _ = Group.objects.get_or_create(name="Студенты")

        # Получаем разрешения для моделей Course и Lesson
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)


        # Администраторам предоставлен полный доступ
        admin_group.permissions.set(Permission.objects.all())

        # Преподаватели могут создавать, редактировать, просматривать и удалять свои курсы, уроки
        teacher_permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=["add_course", "view_course", "change_course", "delete_course",
                          "add_lesson", "view_lesson", "change_lesson", "delete_lesson",
                          ]
        )
        teacher_group.permissions.set(teacher_permissions)

        # Студенты могут только просматривать
        student_permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct], codename__in=["view_course", "view_lesson"]
        )
        student_group.permissions.set(student_permissions)

        self.stdout.write(self.style.SUCCESS("Группы и права успешно созданы."))