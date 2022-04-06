Запуск проекта:
    1. Установить питон 3.10!
    2. Установать зависимости (файл requirements.txt)
        2.0. Использую для команд Git bash windows
        2.1. Создать виртуальное окружение python:
            py -m venv venv
        2.2. Активировать:
            source venv/Scripts/activate
        2.3. Обновить pip:
            py -m pip install --upgrade pip
        2.4. Установить зависимости:
            pip install -r requirements.txt
    3. Запустить проект:
        3.0. Установить зависимости
        3.1. Написать команду:
            py manage.py runserver
    4. Завершение работы:
        4.1. Выключить Джанго:
            Ctrl+C
        4.2. Выключить venv:
            deactivate



Настройка сборщика SASS (.scss):
    (Используется VS Code)
    1) Установить плагин Live Sass Compiler (его ID: ritwickdey.live-sass)
    2) Нажать на комбинацию клавишь ctrl+shift+P 
    3) Выбрать Open Settings (JSON)
    4) Вставить внутрь первых фигурных скобок (не забудте добавить запятую, если она нужна по правилам синтаксиса JSON):
    
    "liveSassCompile.settings.generateMap": false,
    "liveSassCompile.settings.formats": [
        {
            "format": "compressed",
            "autoprefix": "last 5 versions",
            "extensionName": ".css",
            "savePath": "static"
        }
    ],

    5) Запустить сборщик Watсh Sass (справа внизу на панели нажать на кнопку)
    

Админ панель:
    url: http://localhost:8000/admin
    Email: admin@gmail.com
    Password: 123