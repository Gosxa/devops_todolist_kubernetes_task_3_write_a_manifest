# Используем официальный образ Python
FROM python:3.8-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY src/ .

# Настройка для статических файлов (опционально)
ENV STATIC_ROOT=/app/staticfiles

# Открываем порт 8000
EXPOSE 8000

# Запускаем миграции и сервер при старте контейнера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
