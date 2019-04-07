port := 8000
pyfiles := $(wildcard *.py) $(wildcard **/*.py)

.PHONY: bootstrap
bootstrap:
	@pip install -r requirements.txt

.PHONY: lint
lint:
	@find scaffolding/ -name '*.py' | xargs pylint --rcfile pylintrc -j 0

.PHONY: clean
clean:
	@find . -name *.pyc | xargs rm -rf
	@find . -name __pycache__ | xargs rm -rf

.PHONY: deploy
deploy:
	@PYTHON_ENV=production PORT=$(port) docker-compose up -d

.PHONY: teardown
teardown:
	@PORT=$(port) docker-compose down --rmi local

dist: $(pyfiles)
	@pip wheel --wheel-dir=dist --no-deps .

.PHONY: build
build: dist

.PHONY: install
install:
	@pip install --upgrade --force-reinstall --no-deps --no-index --find-links=dist scaffolding
