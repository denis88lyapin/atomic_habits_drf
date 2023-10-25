Приложение atomic_habit_drf. 

Инструкция по запуску.
Шаг 1. Клонировать репозиторий.
Шаг 2. Установить зависимости.
Шаг 3. Создать файл '.env'.
Шаг 4. Создать TG-бота и получить API_KEY.
Шаг 5. Заполнить переменные окружения по образцу в файле '.env.sample'.
    # SECRET_KEY='django-insecure--qo-_rjhy%w*$-ll^%3d(vrs$sah(ghv(&331v&g))o=v46r#d'
    # переменные с типом bool - 1 = True
Шаг 6. Установить postgresql.
Шаг 7. Установить redis.
Шаг 8. Применить миграции.
Шаг 9. Создать суперпользователя:
    python manage.py csu
    # username = "admin"
    # password = "admin"
Шаг 10. Создать пользователей: 
    python manage.py fill_usr
    user1
    # username = "test_1"
    # password = "test1"
    user2
    # username = "test_2"
    # password = "test2"
Шаг 11. Создать TG-бота и получить для пользователей chat_id.
Шаг 12. Запустить сервер.
Шаг 13. Обновить данные пользователей с chat_id.
Шаг 14. Создать привычки.
Шаг 15. Запустить задачи celery:
    celery -A config worker -l INFO
    celery -A config beat -l info -S django
Шаг 16. Тестирование:
    coverage run --source='.' manage.py test
    coverage report --show-missing
