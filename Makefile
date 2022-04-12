.DEFAULT_GOAL := helper
GIT_COMMIT ?= $(shell git rev-parse --short=12 HEAD || echo "NoGit")
BUILD_TIME ?= $(shell date -u '+%Y-%m-%d_%H:%M:%S')
TEXT_RED = \033[0;31m
TEXT_BLUE = \033[0;34;1m
TEXT_GREEN = \033[0;32;1m
TEXT_NOCOLOR = \033[0m

IMAGE = informant

helper: # Adapted from: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "Available targets..." # @ will not output shell command part to stdout that Makefiles normally do but will execute and display the output.
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Builds the application
	docker build -t $(IMAGE) .

test: build ## Builds and then runs tests against the application

genData: ## Generate the test data
	cd tests; cp example_cloud_trails.json /tmp/ && gzip /tmp/example_cloud_trails.json && cd /tmp && tar cvf /tmp/example_cloud_trails.tar example_cloud_trails.json.gz && gzip /tmp/example_cloud_trails.tar && cp /tmp/example_cloud_trails.tar.gz ~

prod: ## Runs the prod version of the application
	docker run -dit -e ENV=prod --network=host $(IMAGE)

dev: ## Runs a dev version of the application
	docker run --name informant --rm -it -e ENV=test --network=host $(IMAGE)

clean: ## Cleans up any old/unneeded items
	-docker stop informant
	-docker rm informant
