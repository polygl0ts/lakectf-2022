DOCKER ?= sudo docker

.PHONY: help build run clean distclean

all: run

help: ## Show this help
	@grep -E -h '\s##\s' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: Dockerfile compose.yaml ## Build the container and the binary
	@$(DOCKER) compose build
	@$(DOCKER) compose run --rm such-sections-builder

run: compose.yaml ## Run the challenge container
	@$(DOCKER) compose up -d

clean: compose.yaml ## Stop the challenge container
	@$(DOCKER) compose down --remove-orphans

distclean: clean ## Stop the challenge container and delete the images
	-rm -f sections
	@$(DOCKER) rmi lakectf-pwn-such-sections:latest lakectf-pwn-such-sections:build
