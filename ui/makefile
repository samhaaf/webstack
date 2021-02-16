
set-stage:
ifeq ($(stage), )
	@echo WARNING: stage variable unspecified. Using 'stage=local'
stage := local
endif


install:
ifeq ($(shell which npm), )
	@echo installing npm
	@sudo apt install npm
endif


config: set-stage
	cd ../config && make apply stage=$(stage) path=../ui


build: install config
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


dev: build
	npm run dev


deploy: build
	@poetry run python bin/sync_to_s3.py
