dc-up:
	docker compose up -d

dc-build:
	docker compose up -d --build

dc-down:
	docker compose down --remove-orphans

dc-restart: dc-down dc-up

migrate:
	docker compose exec backend python manage.py migrate

test:
	docker compose exec backend python manage.py test