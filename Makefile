SERVER_DIR = server

install:
	@poetry env use 3.10.5
	@poetry install --no-root
	@poetry run python $(SERVER_DIR)/environments.py && echo .env successfully created

.PHONY: run
run:
	@poetry run python ./${SERVER_DIR}/app.py --debug
