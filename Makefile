ENV_PATH := .env
PATH := $(ENV_PATH)/bin:${PATH}


env:
	@virtualenv $(ENV_PATH)
	@pip install -r requirements.txt

clean:
	@coverage erase
	@find . -name '*.pyc' -delete

distclean:
	@rm -rf $(ENV_PATH)

test:
	@python setup.py test

coverage:
	@coverage run --source=collection_json --branch setup.py test
	@coverage report -m

lint:
	@flake8 --statistics collection_json.py tests.py


.PHONY: env clean distclean test coverage lint
