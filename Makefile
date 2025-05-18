run-integration-tests:
	python -m pytest test/integration

run-unit-tests:
	python -m pytest test/unit

run-api-tests:
	python -m pytest test/api

run-server-local:
	uvicorn src.main:app --reload --log-config=log_conf.yaml --port 8000

run-server-docker:
	docker compose up fastapi-server

make run-postgres-background:
	docker compose up -d postgres-dev
