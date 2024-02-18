run:
	docker compose up -d
	uvicorn main:app --reload

test:
	pytest tests

lint:
	flake8

build:
	docker build -t myapp .

deploy:
	kubectl apply -f deployment.yaml

.PHONY: run test lint build deploy