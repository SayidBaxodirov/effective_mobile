# 📦 effective_mobile

Python Django задание для Effective Mobile.

## 🌐 API обмена предложениями

Проект реализован на базе **Django REST Framework** и предназначен для обработки предложений обмена между объявлениями (ads). Пользователи могут:

- создавать предложения обмена;
- принимать или отклонять предложения;
- фильтровать и искать предложения;
- использовать **JWT-аутентификацию** для доступа к защищённым маршрутам.

---

## 🚀 Установка и запуск

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/SayidBaxodirov/effective_mobile.git
cd effective_mobile
```
2. **Создайте виртуальное окружение и установите зависимости**
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. **Примените миграции**
```
python manage.py migrate
```
4. **Запустите тесты:**
```
python manage.py test
```
5. **Создайте суперпользователя:**
```
python manage.py createsuperuser
Вам будет предложено ввести username, email и password.
```
6. **Запустите сервер:**
```
python manage.py runserver
```
## 🧪 Документация и тестирование API
После запуска проекта документация Swagger доступна по адресу:
http://127.0.0.1:8000/
### Для доступа к защищённым эндпоинтам:
1. **Получите пару токенов через:**
POST /api/token/
2. **Вставьте ваш access token в Swagger, добавив перед ним слово Bearer, например:**\
Bearer youraccesstoken

**Теперь вы можете использовать POST, PUT, PATCH, DELETE.**

__Чтобы выйти:__
GET /api/logout/
## 📫 Обратная связь
Aвтор: __Sayidabdullaxon Baxodirov__



