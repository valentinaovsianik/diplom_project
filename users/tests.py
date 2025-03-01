from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class UserTests(APITestCase):
    def setUp(self):
        """Создаем пользователей и роли для тестирования"""
        self.admin_group = Group.objects.create(name="Администраторы")
        self.teacher_group = Group.objects.create(name="Преподаватели")
        self.student_group = Group.objects.create(name="Студенты")

        self.admin_user = User.objects.create(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
        )
        self.admin_user.set_password("adminpassword")  # Хешируем пароль
        self.admin_user.save()
        self.admin_user.groups.add(self.admin_group)

        self.teacher_user = User.objects.create(
            email="teacher@example.com",
            password="teacherpassword",
            first_name="Teacher",
            last_name="User",
        )
        self.teacher_user.set_password("teacherpassword")  # Хешируем пароль
        self.teacher_user.save()
        self.teacher_user.groups.add(self.teacher_group)

        self.student_user = User.objects.create(
            email="student@example.com",
            password="studentpassword",
            first_name="Student",
            last_name="User",
        )
        self.student_user.set_password("studentpassword")  # Хешируем пароль
        self.student_user.save()
        self.student_user.groups.add(self.student_group)

        self.register_data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "first_name": "New",
            "last_name": "User",
        }

    def test_user_registration(self):
        """Тестирование регистрации нового пользователя"""
        response = self.client.post("/users/register/", self.register_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        new_user = User.objects.get(email="newuser@example.com")
        self.assertTrue(new_user.check_password("newpassword"))

    def test_user_login(self):
        """Тестирование логина пользователя с JWT"""
        response = self.client.post(
            "/users/login/", {"email": "admin@example.com", "password": "adminpassword"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_admin_permission(self):
        """Тестирование доступа для администратора"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_permission(self):
        """Тестирование доступа для преподавателя"""
        self.client.force_authenticate(user=self.teacher_user)
        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_permission(self):
        """Тестирование доступа для студента"""
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access_for_anonymous(self):
        """Тестирование доступа для неавторизованного пользователя"""
        response = self.client.get("/users/user/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        """Тестирование обновления JWT токена"""
        refresh = RefreshToken.for_user(self.admin_user)
        response = self.client.post("/users/token/refresh/", {"refresh": str(refresh)}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
