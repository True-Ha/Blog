<h2 align="center">Blog_project</h2>

### Описание проекта
Блог с авторизацией, правами доступа для авторов и обычных посетителей, CRUD


**Стек**
- Python >= 3.10
- Django >= 4.1.7
- sqlite3

Установка

pip install req.txt

Старт

python manage.py runserver

## Разработка
#### 1) Поставить звездочку)
#### 2) Клонировать репозиторий
git clone https://github.com/True-Ha/Blog.git

#### 3) Создать виртуальное окружение
cd kino_project

python -m venv venv
#### 4) Активировать виртуальное окружение
Linux:
source venv/bin/activate
Windows:
./venv/Scripts/activate
#### 5) Устанавливить зависимости:
pip install -r req.txt
#### 6) Выполнить команду для выполнения миграций
python manage.py migrate
#### 8) Создать суперпользователя
python manage.py createsuperuser
#### 9) Запустить сервер
python manage.py runserver
#### 10) Ссылки
Сайт http://127.0.0.1:8000/

Админ панель http://127.0.0.1:8000/admin

