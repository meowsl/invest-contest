
install:
	@python -m venv .venv
	@poetry env use 3.10.5
	@poetry install --no-root

.PHONY: run
run:
	@poetry run python ./app.py --debug
