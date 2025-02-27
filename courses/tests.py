from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Answer, Course, Lesson, Question, Test
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        """Настройка тестовой среды"""
        # Создаем группы
        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        # Создаем пользователей
        self.admin = User.objects.create(email="admin@example.com", password="password123")
        self.teacher = User.objects.create(email="teacher@example.com", password="password123")
        self.student = User.objects.create(email="student@example.com", password="password123")

        # Добавляем пользователей в группы
        self.admin.groups.add(self.admin_group)
        self.teacher.groups.add(self.teacher_group)
        self.student.groups.add(self.student_group)

        # Создаем курс
        self.course = Course.objects.create(name="Тестовый курс", description="Описание курса", owner=self.teacher)

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title="Тестовый урок", content="Описание урока", course=self.course, owner=self.teacher
        )

        # URL-ы API
        self.lesson_list_url = "/courses/lessons/"
        self.lesson_create_url = "/courses/lessons/create/"
        self.lesson_detail_url = f"/courses/lessons/{self.lesson.id}/"
        self.lesson_update_url = f"/courses/lessons/{self.lesson.id}/update/"
        self.lesson_delete_url = f"/courses/lessons/{self.lesson.id}/delete/"

    def test_lesson_list(self):
        """Тест получения списка уроков"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        """Тест создания урока (только для преподавателя)"""
        self.client.force_authenticate(user=self.teacher)
        data = {"title": "Новый урок", "content": "Описание", "course": self.course.id}
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create_forbidden(self):
        """Студент не может создавать уроки"""
        self.client.force_authenticate(user=self.student)
        data = {"title": "Запрещенный урок", "content": "Описание", "course": self.course.id}
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_retrieve(self):
        """Тест получения информации о конкретном уроке"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)

    def test_lesson_update(self):
        """Преподаватель может обновлять уроки"""
        self.client.force_authenticate(user=self.teacher)
        data = {"title": "Обновленный урок"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Обновленный урок")

    def test_lesson_update_forbidden(self):
        """Студент не может обновлять уроки"""
        self.client.force_authenticate(user=self.student)
        data = {"title": "Запрещенное изменение"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete(self):
        """Преподаватель может удалять уроки"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_delete_forbidden(self):
        """Студент не может удалять уроки"""
        self.client.force_authenticate(user=self.student)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestApiViewsTests(APITestCase):
    def setUp(self):
        """Настройка тестовой среды"""
        # Создаем группы
        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        # Создаем пользователей
        self.admin = User.objects.create(email="admin@example.com", password="password123")
        self.teacher = User.objects.create(email="teacher@example.com", password="password123")
        self.student = User.objects.create(email="student@example.com", password="password123")

        # Добавляем пользователей в группы
        self.admin.groups.add(self.admin_group)
        self.teacher.groups.add(self.teacher_group)
        self.student.groups.add(self.student_group)

        # Создаём курс, урок и тест
        self.course = Course.objects.create(name="Курс", description="Описание курса", owner=self.teacher)
        self.lesson = Lesson.objects.create(
            title="Урок 1", content="Описание урока", course=self.course, owner=self.teacher
        )
        self.test = Test.objects.create(
            title="Тест 2", description="Содержание теста", owner=self.teacher, lesson=self.lesson
        )

        # URL-ы API
        self.test_list_url = "/courses/tests/"
        self.test_create_url = "/courses/tests/create/"
        self.test_detail_url = f"/courses/tests/{self.test.id}/"
        self.test_update_url = f"/courses/tests/{self.test.id}/update/"
        self.test_delete_url = f"/courses/tests/{self.test.id}/delete/"

    def test_list_tests(self):
        """Тестирование списка тестов (доступ для всех ролей)"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.test_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_test(self):
        """Тестирование создания теста (доступ для преподавателя и администратора)"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(
            self.test_create_url,
            {"title": "Новый тест", "description": "Содержание нового теста", "lesson": self.lesson.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.admin)
        response = self.client.post(
            self.test_create_url,
            {"title": "Еще один тест", "description": "Содержание еще одного теста", "lesson": self.lesson.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(user=self.student)
        response = self.client.post(self.test_create_url, {"title": "Попытка создания", "lesson": self.lesson.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_test(self):
        """Тестирование получения информации о тесте (доступ для всех)"""
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.test_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_test(self):
        """Тестирование обновления теста (только для преподавателя и администратора)"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.test_update_url, {"title": "Обновленный тест"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.test_update_url, {"title": "Админ обновил"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(user=self.student)
        response = self.client.patch(self.test_update_url, {"title": "Студент пробует"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_test(self):
        """Тестирование удаления теста (только для преподавателя и администратора)"""
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(self.test_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.test = Test.objects.create(
            title="Тест 2", description="Содержание теста", owner=self.teacher, lesson=self.lesson
        )
        self.test_delete_url = f"/courses/tests/{self.test.id}/delete/"

        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.test_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.test = Test.objects.create(
            title="Тест 3", description="Содержание третьего теста", owner=self.teacher, lesson=self.lesson
        )
        self.test_delete_url = f"/courses/tests/{self.test.id}/delete/"

        self.client.force_authenticate(user=self.student)
        response = self.client.delete(self.test_delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestQuestionApiViews(APITestCase):
    """Настройка тестовой среды для тестироания представлений модели ответов"""

    def setUp(self):
        self.admin = User.objects.create(email="admin@example.com", password="password123")
        self.teacher = User.objects.create(email="teacher@example.com", password="password123")
        self.student = User.objects.create(email="student@example.com", password="password123")

        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.admin.groups.add(self.admin_group)
        self.teacher.groups.add(self.teacher_group)
        self.student.groups.add(self.student_group)

        self.course = Course.objects.create(name="Курс", description="Описание курса", owner=self.teacher)
        self.lesson = Lesson.objects.create(
            title="Урок 1", content="Описание урока", course=self.course, owner=self.teacher
        )
        self.test = Test.objects.create(
            title="Тест 1", description="Содержание теста 1", owner=self.teacher, lesson=self.lesson
        )
        self.question = Question.objects.create(test=self.test, text="Это первый вопрос теста?")

        self.question_list_url = "/courses/questions/"
        self.question_create_url = "/courses/questions/create/"
        self.question_detail_url = f"/courses/questions/{self.question.id}/"
        self.question_update_url = f"/courses/questions/{self.question.id}/update/"
        self.question_delete_url = f"/courses/questions/{self.question.id}/delete/"

    def test_list_questions(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(self.question_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(self.question_create_url, {"test": self.test.id, "text": "Сейчас 2025 год?"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_question(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.question_update_url, {"text": "Это вопрос для выполнения теста?"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_question(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(self.question_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAnswerApiViews(APITestCase):
    """Настройка тестовой среды для тестироания представлений модели ответов"""

    def setUp(self):
        self.admin = User.objects.create(email="admin@example.com", password="password123")
        self.teacher = User.objects.create(email="teacher@example.com", password="password123")
        self.student = User.objects.create(email="student@example.com", password="password123")

        self.admin_group, _ = Group.objects.get_or_create(name="Администраторы")
        self.teacher_group, _ = Group.objects.get_or_create(name="Преподаватели")
        self.student_group, _ = Group.objects.get_or_create(name="Студенты")

        self.admin.groups.add(self.admin_group)
        self.teacher.groups.add(self.teacher_group)
        self.student.groups.add(self.student_group)

        self.course = Course.objects.create(name="Курс", description="Описание курса", owner=self.teacher)
        self.lesson = Lesson.objects.create(
            title="Урок 1", content="Описание урока", course=self.course, owner=self.teacher
        )
        self.test = Test.objects.create(
            title="Тест 1", description="Содержание теста 1", owner=self.teacher, lesson=self.lesson
        )
        self.question = Question.objects.create(test=self.test, text="Это первый вопрос теста?")
        self.answer = Answer.objects.create(question=self.question, text="Да", is_correct=True)

        self.answer_list_url = "/courses/answers/"
        self.answer_create_url = "/courses/answers/create/"
        self.answer_detail_url = f"/courses/answers/{self.answer.id}/"
        self.answer_update_url = f"/courses/answers/{self.answer.id}/update/"
        self.answer_delete_url = f"/courses/answers/{self.answer.id}/delete/"

    def test_list_answers(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.answer_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_answer(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(
            self.answer_create_url, {"question": self.question.id, "text": "Нет", "is_correct": False}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_answer(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.patch(self.answer_update_url, {"text": "Да"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_answer(self):
        self.client.force_authenticate(user=self.teacher)
        response = self.client.delete(self.answer_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
