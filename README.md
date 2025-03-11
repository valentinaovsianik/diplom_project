# Платформа для самообучения  

Платформа предоставляет возможность авторизации и аутентификации пользователей, управление курсами и уроками, а также тестирование знаний.  


## Функционал  

- **Авторизация и аутентификация** (JWT)  
- **CRUD** для курсов, уроков, тестов и вопросов  
- **Роли и права доступа** (Администратор, Преподаватель, Студент)  
- **Студенты** могут просматривать курсы, уроки и проходить тесты  
- **Преподаватели** могут управлять своими курсами, уроками и тестами  
- **Администраторы** имеют полный доступ ко всему  
- **Автогенерируемая документация API** (Swagger)  
- **Настроен CORS**
- **Тестирование кода**  
- **Разработано с использованием Django + DRF + PostgreSQL**


## Структура проекта  

Проект Django включает два приложения:

- **`courses`** – управление курсами, уроками и тестами  
- **`users`** – управление пользователями и ролями  

Конфигурация проекта находится в директории **config**.


### Основные модели:  

- **`Course`** – курсы  
- **`Lesson`** – уроки  
- **`Test`** – тесты  
- **`Question`** – вопросы теста  
- **`Answer`** – ответы на вопросы  
- **`TestResult`** – результаты тестирования  


## Установка
Клонируйте репозиторий:
git@github.com:valentinaovsianik/diplom_project.git


## Как запустить:
После клонирования репозитория и установки зависимостей выполните **python manage.py runserver**.


## Тестирование:
Запустить подсчет покрытия кода тестами и вывести отчет можно, выполнив **coverage run --source='.' manage.py test**
и **coverage report**.


## Документация:
Описание проекта в файле **README.md**, также есть комментарии в коде. Подключена автогенерируемая документация API с использованием Swagger, которая доступна по адресу адресу http://127.0.0.1:8000/swagger.


## Лицензия:
На проект распространяется [лицензия MIT](LICENSE).
