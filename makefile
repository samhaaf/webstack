# stage := 'local'
# db_name := $(jq '.database.db_name' ./config/stages/$(stage).private.json)
# username := $(jq '.postgres.username' ./config/stages/$(stage).private.json)
# password := $(jq "'.postgres.password'" ./config/stages/$(stage).private.json)

assert-stage:
ifeq ($(stage), )
	$(error stage argument required for this make method)
endif


install:
ifeq (, $(shell which poetry))
	@echo installing python-poetry
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
endif
	sudo apt install jq docker
	poetry install


# build-db:
	# @echo $(username)
	# @echo $(db_name)
	# @echo $(password)
	# @echo
	#@docker run --name $(db_name) -e POSTGRES_PASSWORD=$(password) -d postgres


config-api: assert-stage
	poetry run python config/bin/apply.py -i api/ --pretty --stage $(stage)

config-ui: assert-stage
	poetry run python config/bin/apply.py -i ui/ --pretty --stage $(stage)

config-print:
ifeq ($(stage), )
	@poetry run python config/bin/generate.py
else
	@poetry run python config/bin/generate.py --stage $(stage)
endif
