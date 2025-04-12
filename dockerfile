FROM python:3.10-slim

# Устанавливаем зависимости для psycopg2
RUN apt-get update && apt-get install -y libpq-dev

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение в контейнер
COPY . .

# Открываем порт для приложения
EXPOSE 5000

# Запускаем приложение
CMD ["python3", "run.py"]
