all:

# docker
start:
	@echo "bringing up project...."
	docker compose up

fresh:
	@echo "bringing down project...."
	docker compose down -v
    docker-compose build
    start

bash:
	@echo "connecting to container...."
	docker compose exec kaffepause_api bash

# lint
test:
	@echo "running pytest...."
	docker compose exec kaffepause_api pytest --cov-report xml --cov=src tests/

lint:
	@echo "running ruff...."
	docker compose exec kaffepause_api ruff src

black:
	@echo "running black...."
	docker compose exec kaffepause_api black .

mypy:
	@echo "running mypy...."
	docker compose exec kaffepause_api mypy src/

hooks: check
	@echo "installing pre-commit hooks...."
	pre-commit install
