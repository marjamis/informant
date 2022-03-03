.DEFAULT_GOAL := helper
GIT_COMMIT ?= $(shell git rev-parse --short=12 HEAD || echo "NoGit")
BUILD_TIME ?= $(shell date -u '+%Y-%m-%d_%H:%M:%S')
TEXT_RED = \033[0;31m
TEXT_BLUE = \033[0;34;1m
TEXT_GREEN = \033[0;32;1m
TEXT_NOCOLOR = \033[0m

helper: # Adapted from: https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@echo "Available targets..." # @ will not output shell command part to stdout that Makefiles normally do but will execute and display the output.
	@grep -hE '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

command:
	@echo "Hello $(NAME)"

build: ## Builds the application
	docker build -t informant .

test: build ## Builds and then runs tests against the application
	# TODO break into unit tests and full testing and profiling
	golint ./...
	go test -v -coverprofile cp.out ./...
	go tool cover -html=cp.out

	go test -cpuprofile cpu.prof -memprofile mem.prof <package>
	go tool pprof -http=":8081" cpu.prof &
	go tool pprof -http=":8082" mem.prof &

run: ## Runs the prod version of the application
	# $(MAKE) command NAME="marjamis"docker run -it informant
	docker run --rm -it --network=host informant

dev: ## Runs a dev version of the application
	$(MAKE) command NAME="devTester"

clean: ## Cleans up any old/unneeded items
	-rm exampleFile # - means ignore this line on failure, such as if the file doesn't exist.
