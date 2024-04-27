SERVER_DIR = server
MODEL_DIR = train_models

install:
	@poetry env use 3.10.5
	@poetry install --no-root
	@poetry run python $(SERVER_DIR)/environments.py && echo .env successfully created
	@.venv\Scripts\pip install -r .\requirements.txt

.PHONY: run
run:
	@poetry run python -B ./${SERVER_DIR}/app.py --debug

.PHONY: train
train:
	@poetry run python -B ./${MODEL_DIR}/train.py

.PHONE: test-models
test-models:
	@poetry run python -B ./${MODEL_DIR}/test.py