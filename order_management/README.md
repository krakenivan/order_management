# Менеджер заказов в кафе

## 📌 Описание
Данный проект помогает управлять заказами в кафе, а именно:
- добавление заказов
- поиск заказов
- вывод таблицы заказов
- удаление заказов
- смена статуса заказов
- показ выручки и не оплаченных заказов
- работать с меню (добавлять и удалять блюда)
- редактировать заказы

## 🚀 Технологии
Список используемых технологий:
- Python 3.13
- Django 5.1.5
- SQLite3

## 📂 Структура проекта
Проект разделен на приложение, каждое из которых отвечает за свой функционал:

- home - главная страница
- add_order_app - для добавления заказов в БД
- calculation_app - для показа выручки и вывода доп информации
- change_status_app - для смены статуса заказа
- delete_order_app - для удаления заказа из БД
- find_order_app - для поиска заказа по id или номеру стола
- show_order_app - для вывода информации о всех заказах
- list_product_app - для работы с меню
- edit_order_app - для изменения заказа
- common - хранит модель основной БД

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



✅ Тестирование

Запуск тестов:
```bash
python manage.py test
```

📝 Автор

👤 [Иван](https://github.com/krakenivan)
