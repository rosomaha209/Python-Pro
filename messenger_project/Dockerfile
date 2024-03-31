# Використовуємо офіційний образ Python як базовий
FROM python:3.12

# Встановлюємо робочий каталог у контейнері
WORKDIR /usr/src/app

# Встановлення Node.js та npm
# Замість того, щоб використовувати curl для встановлення Node.js,
# рекомендується використовувати офіційний образ Node як базовий шар або використати multistage build,
# але для спрощення ми продовжимо з цим підходом.
RUN apt-get update && apt-get install -y --fix-missing curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get update && apt-get install -y nodejs npm


# Копіюємо файли залежностей Python і встановлюємо їх
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Встановлення Flower для Celery моніторингу (якщо потрібно)
RUN pip install flower

# Копіюємо файли залежностей NPM і встановлюємо їх
COPY package.json package-lock.json ./
RUN npm install

# Копіюємо весь решту коду додатку у контейнер
COPY . .

# Виконуємо збирання за допомогою Webpack
RUN npm run build

# Вказуємо, що контейнер слухатиме порт 8000 під час виконання
EXPOSE 8000

# Команда для запуску Django сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
