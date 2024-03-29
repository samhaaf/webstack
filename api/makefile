
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


install: set-default-stage
	@cd .. && make install only_sys_installs=true
ifeq ($(stage), local)
	poetry install --no-dev --remove-untracked
else ifeq ($(stage), dev)
	poetry install --no-dev --remove-untracked
else
	poetry install
endif


build: set-default-stage install
	poetry export -f requirements.txt -o requirements.txt --without-hashes
	cd ../config && make apply stage=$(stage) path=../api


deploy: build
ifeq ($(stage), local)
	$(error Cannot run 'make deploy' using 'stage=local')
else
	poetry run python3 bin/setup_iam.py --stage $(stage)
	poetry run chalice deploy --stage $(stage) --connection-timeout 300
endif


local: build
	poetry run chalice local


check-clean: set-stage
	echo -n "Are you sure you want to clean 'stage=$(stage)'? [y/N] " && read ans && [ $${ans:-N} = y ]


clean: check-clean set-stage
ifeq ($(stage), local)
	$(error Cannot interpret 'make clean' using 'stage=local')
else
	poetry run chalice delete --stage $(stage)
endif
