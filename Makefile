RUNTIME_TAG='pizzaseol-logger-manager'

build: \
	runtime-build

runtime-build:
	docker build --tag ${RUNTIME_TAG} \
	./env/docker/runtime-dev

update-code-only:
	git reset --hard
	git pull

