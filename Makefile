run:
	uvicorn main:app --reload

lint:
	autoflake --remove-all-unused-imports --remove-unused-variables --exclude=venv --in-place --recursive .

.PHONY: run test lint build deploy