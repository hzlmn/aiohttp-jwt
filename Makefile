#
# Makefile for aiohttp-jwt
#

include ./make/print.lib.mk

#------------------------------
# vars
#------------------------------

SHELL := /bin/bash
PWD:=$(shell pwd)
SSH_KEY_NAME ?= $(shell test -e $(HOME)/.ssh/id_ed25519 && echo id_ed25519 || echo id_rsa)

MOUNTED_SSH_KEYS = -v ~/.ssh/${SSH_KEY_NAME}:/${SSH_KEY_NAME}:ro -v ~/.ssh/${SSH_KEY_NAME}.pub:/${SSH_KEY_NAME}.pub:ro
MOUNTED_SSH_AUTH_SOCK := --env SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock -v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock ${MOUNTED_SSH_KEYS}

#------------------------------
# help
#------------------------------

.PHONY: help
help:
	$(call print_h1,"AVAILABLE","OPTIONS")
	$(call print_space)
	$(call print_h2,"docker")
	$(call print_options,"build","Build docker images for development.")
	$(call print_space)
	$(call print_h2,"dependency")
	$(call print_options,"compile-deps","Compile the dependencies from pyproject.toml into a poetry.lock file without updating the existing dependencies.")
	$(call print_space)
	$(call print_h2,"test")
	$(call print_options,"test","Run all tests.")
	$(call print_space)
	$(call print_h2,"code")
	$(call print_options,"lint","Run code lint checks.")
	$(call print_options,"format","Automatically format code where possible.")

#------------------------------
# docker
#------------------------------

.PHONY: build
build:
	$(call print_h1,"BUILDING","IMAGES")
	@docker build --ssh default -t tenproduct/aiohttp_jwt_3_9 --build-arg python_version=3.9 .
	@docker-compose build --parallel
	$(call print_h1,"IMAGES","BUILT")


.PHONY: build-python-3.9
build-python-3.9:
	$(call print_h1,"BUILDING","PYTHON","3.9","IMAGE")
	@docker build --ssh default -t tenproduct/aiohttp_jwt_3_9 .
	@docker-compose build aiohttp_jwt_3_9
	$(call print_h1,"PYTHON","3.9","IMAGE","BUILT")

#------------------------------
# dependency
#------------------------------

.PHONY: compile-deps
compile-deps: build
	$(call print_h1,"COMPILING","REQUIREMENTS")
	docker run --entrypoint= --rm --tty --interactive $(MOUNTED_SSH_AUTH_SOCK) tenproduct/ten_utils_opensearch /bin/bash -l -c 'eval "$$(ssh-agent)" && ssh-add /${SSH_KEY_NAME} && poetry lock --no-update'

#------------------------------
# code
#------------------------------

.PHONY: lint
lint: build-python-3.9
	$(call print_h1,"LINTING","CODE")
	@docker-compose run --rm --entrypoint= aiohttp_jwt_3_9 flake8 .
	@docker-compose run --rm --entrypoint= aiohttp_jwt_3_9 isort --check-only aiohttp_jwt setup.py tests --diff
	$(call print_h1,"LINTING","COMPLETED")

.PHONY: format
format: build-python-3.9
	$(call print_h1,"FORMATTING","CODE")
	@docker-compose run --rm --entrypoint= aiohttp_jwt_3_9 isort aiohttp_jwt setup.py tests
	$(call print_h1,"FORMATTING","COMPLETED")

#------------------------------
# QA
#------------------------------

.PHONY: test
test: build-python-3.9
	$(call print_h1,"RUNNING","ALL","TESTS")
	@docker-compose run --rm --entrypoint= aiohttp_jwt_3_9 pytest tests/
	$(call print_h1,"ALL","TESTS","COMPLETED")
