# Визначте змінні для зручності
DC = docker-compose

# Замініть на команду для запуску вашого додатку, наприклад, для Django:
# DJANGO_RUN = $(DC) run --rm web python manage.py

.PHONY: build up down start stop restart logs ps migrate shell

# Будувати контейнери
build:
	$(DC) build

# Запустити контейнери в фоновому режимі
up:
	$(DC) up -d

# Зупинити та видалити контейнери, мережі, об'єми та образи, створені командою 'up'
down:
	$(DC) down

# Запустити контейнери
start:
	$(DC) start

# Зупинити контейнери
stop:
	$(DC) stop

# Перезапустити контейнери
restart:
	$(DC) restart

# Перегляд логів
logs:
	$(DC) logs -f

# Показати запущені контейнери
ps:
	$(DC) ps

# Виконати міграції, наприклад, для Django
migrate:
	$(DC) run --rm web python manage.py migrate

# Відкрити shell, наприклад, Django shell
shell:
	$(DC) run --rm web python manage.py shell

createsuperuser:
	$(DC) run --rm web python manage.py createsuperuser

test:
	$(DC) run --rm web python manage.py test
