
set-stage:
ifeq ($(stage), )
	@echo WARNING: stage variable unspecified. Using 'stage=local'
stage := local
endif


install:
ifeq ($(shell which docker), )
	@echo installing docker
	sudo apt install docker -y
endif


build: install set-stage
	$(error Not implemented)


deploy: set-stage
ifeq ($(stage), local)
	$(error Not implemented)
else
	$(error Not implemented)
endif
