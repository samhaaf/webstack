

assert-stage:
ifeq ($(stage), )
	$(error Must specify stage argument)
else
	@echo stage=$(stage)
endif


set-default-stage:
ifeq ($(stage), )
	@echo WARNING: stage variable unspecified. Using 'stage=local'
stage := local
endif


install:
ifeq ($(shell which docker), )
	sudo apt install docker.io -y
	sudo usermod -aG docker ${USER}
	sudo docker pull postgres:13.4
endif


build: install set-default-stage
ifeq ($(stage), local)
	poetry run python bin/build_docker.py --stage local
else
	poetry run python bin/build_rds.py --stage $(stage)
endif


start: install set-default-stage
	poetry run python bin/start_docker.py --stage local


stop: set-default-stage
	poetry run python bin/stop_docker.py --stage local


clear: set-default-stage stop
	poetry run python bin/clear_docker.py --stage local


update: set-default-stage
	poetry run python bin/update.py --stage $(stage)


rebuild: set-default-stage
	make -i stop >/dev/null
	make -i clear >/dev/null
	make build >/dev/null
	make start >/dev/null
	@sleep 2
	poetry run python bin/update.py --stage $(stage)
