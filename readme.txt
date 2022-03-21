Запуск проекта:
    1. Установить питон 3.10!
    2. Установать зависимости (файл requirements.txt)
    3. Запустить проект:
        1) Написать команду py manage.py runserver

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