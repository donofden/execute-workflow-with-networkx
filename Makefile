# Makefile for Execute Workflow With NetworkX
#
.DEFAULT_GOAL := explain
explain:
	###     Welcome to Execute Workflow With NetworkX
	@echo " Choose a command to run: "
	@cat Makefile* | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: test
install: ## Install Dependency Packages
	poetry install 

.PHONY: test
test: ## Run Unit Tests
	poetry run python -m pytest -v 

.PHONY: test-cov
test-cov: ## Run tests and create coverage report
	poetry run python -m pytest -v --cov=.
	poetry run python -m coverage report -m;
	poetry run python -m coverage html


