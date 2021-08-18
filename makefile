
set-stage:
ifeq ($(stage), )
	@echo WARNING: stage variable unspecified. Using 'stage=local'
stage := local
endif


install:
ifeq ($(shell which poetry), )
	@echo installing python-poetry
	@curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
endif
ifeq ($(only_sys_installs), )
	poetry install
endif


build: install set-stage
	@echo 'make build' specific items not yet implemented


build-all: build
	cd db && make build stage=$(stage)
	cd api && make build stage=$(stage)
	cd ui && make build stage=$(stage)
