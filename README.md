# Менеджер заказов в кафе

## 📌 Описание
Данный проект помогает управлять заказами в кафе, а именно:
- добавление заказов
- поиск заказов
- вывод таблицы заказов
- удаление заказов
- смена статуса заказов
- показ аналитики заказов
- работать с меню (добавлять и удалять блюда)
- редактировать заказы
- работать со столами
- реализован API для работы с данными

## 🚀 Технологии
Список используемых технологий:
- Python 3.13
- Django 5.1.5
- SQLite3
- Django REST Framework 3.16.0
- Docker

## 📂 Структура проекта
Проект разделен на приложение, каждое из которых отвечает за свой функционал:

- home - главная страница
- add_order_app - для добавления заказов
- calculation_app - для показа аналитики заказов
- change_status_app - для смены статуса заказа
- delete_order_app - для удаления заказа
- find_order_app - для поиска заказов
- show_order_app - для вывода информации о всех заказах
- list_product_app - для работы с меню
- edit_order_app - для изменения заказа
- table_app - для работы со столами
- common - хранит модель основной БД и сервисы
- api - API для работы с основными моделями проекта

Docker и docker-compose.yml для запуска и дальнейшей разработки проекта

## 📦 Установка и настройка

### 🔧 1. Клонирование репозитория
```bash
git clone https://github.com/krakenivan/order_management.git
cd repository
```

🛠 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate  # для Windows
```

📥 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

🚀 4. Применение миграций и запуск проекта
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
После этого проект будет доступен по адресу http://127.0.0.1:8000/
API будет доступен по адресу http://127.0.0.1:8000/api/v1/


✅ Тестирование

Запуск тестов:
```bash
python manage.py test
```


🐳 Запуск Docker
```bash
docker-compose up -d
```


📝 Автор

👤 [Иван](https://github.com/krakenivan)
