
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
	@echo installing docker
	sudo apt install docker -y
endif


build: install set-default-stage
	$(error Not implemented)


deploy: assert-stage
ifeq ($(stage), local)
	$(error Not implemented)
else
	$(error Not implemented)
endif
