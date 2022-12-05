DOCKER ?= sudo -E docker

.PHONY: default build run clean distclean

default: build

build: Dockerfile compose.yaml rev-baby.c
	@$(DOCKER) compose build
	@$(DOCKER) buildx build --target=exporter --output type=local,dest=out .

run:
	@$(DOCKER) compose up

clean:
	@$(DOCKER) compose down

distclean: clean
	@$(DOCKER) rmi rev-baby:latest
	@sudo rm -rf out
