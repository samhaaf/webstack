

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
	sudo docker pull postgres
endif


build: install set-default-stage
	@poetry run python bin/build_docker.py --stage local


start: install set-default-stage
	@poetry run python bin/start_docker.py --stage local


stop: set-default-stage
	@poetry run python bin/stop_docker.py --stage local


clear: set-default-stage stop
	@poetry run python bin/clear_docker.py --stage local


rebuild:
	make -i stop >/dev/null
	make -i clear >/dev/null
	make build >/dev/null
	make start >/dev/null


deploy: assert-stage
ifeq ($(stage), local)
	$(error cannot deploy to stage=local)
else
	$(error Not implemented)
endif
