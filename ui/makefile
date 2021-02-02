
build:
	cd .. && make config-ui stage=$(stage)
	npm install
	npm run build

local: 
	make build stage=local
	@npm run dev

serve: build
	npm run serve

deploy: build
	@poetry run python bin/sync_to_s3.py
