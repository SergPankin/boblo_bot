FROM python:3.8-alpine3.10
LABEL maintainers="SergPankin, Agesyne"

# Устанавливаем зависимости
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

# Задаём текущую рабочую директорию
WORKDIR /boblo_bot_dir
# Копируем код из локального контекста в рабочую директорию образа
COPY . .

RUN pip3 install -r requirements.txt
RUN mkdir -p ~/.postgresql && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
     --output-document ~/.postgresql/root.crt && \
    chmod 0600 ~/.postgresql/root.crt


# Настраиваем команду, которая должна быть запущена в контейнере во время его выполнения
ENTRYPOINT ["python3.8", "main.py"]
