# Система Управления Заказами в Кафе на Django

## Описание

Веб-приложение для управления заказами в кафе, разработанное на Django.  Позволяет добавлять, удалять, искать, изменять и отображать заказы.

## Технологии

*   Python 3.8+
*   Django 4+ / DRF
*   HTML / CSS / Bootstrap
*   SQLite

## Установка

1.  Клонируйте репозиторий:

    ```bash
    git clone https://github.com/mrMaks2/cafe_orders_with_API.git
    cd cafe_management
    ```

2.  Создайте виртуальное окружение:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows
    ```

3.  Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4.  Примените миграции:

    ```bash
    python manage.py migrate
    ```

5.  Создайте суперпользователя:

    ```bash
    python manage.py createsuperuser
    ```

6.  Запустите сервер разработки:

    ```bash
    python manage.py runserver
    ```

7.  Откройте приложение в браузере: `http://127.0.0.1:8000/`

## Использование

*   Перейдите в административную панель по адресу `http://127.0.0.1:8000/admin/` и войдите, используя учетные данные суперпользователя.
*   Используйте веб-интерфейс для управления заказами.

## API

Доступны следующие endpoint'ы REST API:

*   `GET /api/orders/`:  Получение списка всех заказов.
*   `POST /api/orders/`:  Создание нового заказа.
*   `GET /api/orders/<id>`: Получение информации о заказе с указанным ID.
*   `DELETE /api/orders/<id>/`: Удаление заказа с указанным ID.
*   `GET /api/orders/?search=<Номер стола или статус заказа>/`: Поиск заказов по номеру стола или по статусу заказа.
