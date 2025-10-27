.PHONY: build up down restart logs clean ps migrate-config install dev

# Build the Docker image
build:
	docker-compose build

# Run the container in detached mode
up:
	docker-compose up -d --build

# Stop the container
down:
	docker-compose down

# Restart the container
restart: down up

# View container logs
logs:
	docker-compose logs -f 

# Remove containers, networks, and images
clean:
	docker-compose down --rmi all --volumes --remove-orphans

# Show running containers
ps:
	docker-compose ps

# Migrate configuration from .env to YAML
migrate-config:
	python scripts/migrate_config.py

# Install dependencies
install:
	poetry install

# Development setup
dev: install
	cp config.example.yml config.yml
	@echo "Configuration template created. Please edit config.yml with your settings."

