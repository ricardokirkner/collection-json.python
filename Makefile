ENV_PATH := .env
PATH := $(ENV_PATH)/bin:${PATH}


env:
	@virtualenv $(ENV_PATH)
	@pip install -r requirements.txt

clean:
	@rm .coverage

distclean:
	@rm -rf $(ENV_PATH)

test:
	@nosetests -vs

coverage:
	@nosetests -vs --with-coverage --cover-package=collection_json --cover-branches

lint:
	@flake8 --statistics collection_json.py tests.py


.PHONY: env clean distclean test coverage lint
