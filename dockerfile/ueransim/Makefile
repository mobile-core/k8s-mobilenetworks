# Makefile
DOCKER_ENV              ?= DOCKER_BUILDKIT=1
DOCKER_TAG              ?= 3.1.9
DOCKER_REGISTRY         ?= docker.io
DOCKER_REPOSITORY       ?= monandkey/ueransim
DOCKER_BUILD_ARGS       ?= --rm

FREE5GC_CLI_IMAGE_NAME  ?= ${DOCKER_REGISTRY}/${DOCKER_REPOSITORY}:${DOCKER_TAG}

build-all: build-ueransim

.PHONY: build-ueransim
build-ueransim: 
	${DOCKER_ENV} docker build ${DOCKER_BUILD_ARGS} \
		--tag ${FREE5GC_CLI_IMAGE_NAME} \
		--file ./Dockerfile \
		--no-cache \
		./

# Sample Command
# DOCKER_BUILDKIT=1 docker build --rm \
#   --tag docker.io/monandkey/ueransim:0.4 \
#   --file ./Dockerfile \
#   --no-cache \
#   ./