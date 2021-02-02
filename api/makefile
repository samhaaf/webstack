build:
	poetry install --no-dev --remove-untracked
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	cd .. && make config-api stage=$(stage)

build-local:
	poetry install
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	cd .. && make config-api stage=local

# activate:
# 	@poetry shell

deploy: build
	poetry run chalice deploy

# deploy: build-dev
# 	poetry run chalice deploy

local: build-local
	poetry run chalice local

destroy:
	poetry run chalice delete
