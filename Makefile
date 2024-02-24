run:
	docker compose up -d
	uvicorn main:app --reload

lint:
	autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .

.PHONY: run test lint build deploy