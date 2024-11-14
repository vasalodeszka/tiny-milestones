# Set default environment to 'local' if none is provided
ENV ?= local

# Default target: show available commands when no target is specified
help:
	@echo "Available commands:"
	@echo "  make up ENV=local|prod                            - Bring up the services with Docker Compose (--build)"
	@echo "  make down ENV=local|prod                          - Bring down the services"
	@echo "  make createsuperuser ENV=local|prod               - Create a Django superuser"
	@echo "  make migrations ENV=local|prod                	   - Make Django migrations"
	@echo "  make migrate ENV=local|prod                       - Apply Django migrations"
	@echo "  make shell ENV=local|prod                         - Start bash shell"

# Command to bring up the services with --build option based on the environment
up:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml up --build -d
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml up --build -d
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif

# Command to bring down the services based on the environment
down:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml down
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml down
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif

# Command to run createsuperuser with the appropriate docker-compose file
createsuperuser:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml run --rm django python manage.py createsuperuser
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml run --rm django python manage.py createsuperuser
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif

# Command to run makemigrations with the appropriate docker-compose file
migrations:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml run --rm django python manage.py makemigrations
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml run --rm django python manage.py makemigrations
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif

# Command to run migrate with the appropriate docker-compose file
migrate:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml run --rm django python manage.py migrate
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml run --rm django python manage.py migrate
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif

# Command to run bash shell with the appropriate docker-compose file
shell:
ifeq ($(ENV),local)
	@docker compose -f docker-compose.local.yaml run --rm django bash
else ifeq ($(ENV),prod)
	@docker compose -f docker-compose.production.yaml run --rm django bash
else
	@echo "Invalid ENV value! Please specify ENV=local or ENV=prod."
	exit 1
endif
