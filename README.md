# boblo_bot
Here I store my pet bot

Prerequirements:
1. ВМ на облаке
2. PostgreSQL 14 на облаке (+ заполнить кредами config-template)
3. Токен бота
4. Python >= 3.7
5. Доп команды, если делаете с нуля:
sudo apt-get install postgresql
sudo apt-get install libpq-dev

Запуск:
1. Скопировать миграции в БД в облаке
2. Установить зависимости
3. Запускать на ВМ main.py в фоновом режимпе (nohup)

Как запустить на докере:
1. sudo docker build . -t bot/boblo_bot:0.1
3. sudo docker run --rm --name=boblo bot/boblo_bot:0.1
4. sudo docker stop boblo
