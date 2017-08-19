# Requirements / Требования

Для работы требуется:

* python3
* unoconv
* libreoffice

Должны быть установлены библиотеки для python3:

* uno
* django
* nginx
* lxml

# Настройка сервера

## Настройка внутреннего скрипта

В начале нужно изменить переменную

    global_path = 'Your path to folder, where installed project'

Например, digital_signature установлен в папке /home/user/Projects, тогда следует написать в scripts_settings.py:

    global_path = '/home/olof/Projects/digital_signature/base_model/'

## Настройка nginx

Добавьте несколько строчек в /etc/nginx/sites-enabled/default:

    location / {
      proxy_pass http://127.0.0.1:8000;
    }

    location /static/ {
      root /home/user/Projects/digital_signature/base_model/;
    }

Разумеется, '/home/user/Projects/' заменить на собственный путь к проекту

# Запуск сервера

Чтобы запустить сервер, нужно перейти в папку вашего проекта:

    cd /home/user/Projects/digital_signature/base_model

И написать:

    python3 manage.py runserver

Так же в еще одном терминале нужно прописать:

    libreoffice --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager" --headless

Это утилита для работы с xlsx файлами, без неё создание нового заказа не будет работать
