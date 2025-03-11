from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from courses.models import Answer, Course, Lesson, Question, Test, TestResult


class Command(BaseCommand):
    "Создание групп пользователей и назначение им прав"

    def handle(self, *args, **kwargs):
        # Создаём или получаем группы
        admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        student_group, _ = Group.objects.get_or_create(name="Студенты")

        # Получаем разрешения для моделей
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        test_ct = ContentType.objects.get_for_model(Test)
        question_ct = ContentType.objects.get_for_model(Question)
        answer_ct = ContentType.objects.get_for_model(Answer)
        test_result_ct = ContentType.objects.get_for_model(TestResult)

        # Администраторам предоставлен полный доступ
        admin_group.permissions.set(Permission.objects.all())

        # Преподаватели могут выполнять все действия со своими курсами, уроками, тестами
        teacher_permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct, test_ct, question_ct, answer_ct],
            codename__in=[
                "add_course",
                "view_course",
                "change_course",
                "delete_course",
                "add_lesson",
                "view_lesson",
                "change_lesson",
                "delete_lesson",
                "add_test",
                "view_test",
                "change_test",
                "delete_test",
                "add_question",
                "view_question",
                "change_question",
                "delete_question",
                "add_answer",
                "view_answer",
                "change_answer",
                "delete_answer",
            ],
        )
        teacher_group.permissions.set(teacher_permissions)

        # Студенты могут только просматривать курсы, уроки, тесты и вопросы, выполнять тесты
        student_permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct, test_ct, question_ct, test_result_ct],
            codename__in=[
                "view_course",
                "view_lesson",
                "view_test",
                "view_question",
                "add_testresult",
                "view_testresult",
            ],
        )
        student_group.permissions.set(student_permissions)

        self.stdout.write(self.style.SUCCESS("Группы и права успешно созданы."))
