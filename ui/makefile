
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
ifeq ($(shell which npm), )
	@echo installing npm
	@sudo apt install npm
endif


apply-config: set-default-stage
	cd ../config && make apply stage=$(stage) path=../ui


build: install apply-config
	npm install
ifeq ($(stage), local)
	npm run build
else ifeq ($(stage), dev)
	npm run build
else
	npm run build
endif


serve: build
	npm run start


local: build
	npm run dev


deploy: assert-stage build
	@poetry run python bin/build_distribution.py --stage $(stage)
	@poetry run python bin/sync_to_s3.py --stage $(stage)
