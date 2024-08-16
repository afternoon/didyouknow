name = didyouknow
tag = $(name):latest

container_stamp = .container.stamp
lint_stamp = .lint.stamp

.PHONY: all container lint repl run_dev run_docker

all: run_dev

$(container_stamp): Dockerfile pyproject.toml poetry.lock didyouknow/*.py factfile.pickle
	docker build --tag $(tag) .
	touch $(container_stamp)

$(lint_stamp): **/*.py
	ruff format
	ruff check
	touch $(lint_stamp)

container: $(container_stamp)

lint: $(lint_stamp)

repl:
	poetry run python3

run_dev:
	poetry run sanic $(name):app --dev

run_docker: container
	docker run --publish 8000:8000 $(tag)

clean:
	rm $(container_stamp) $(lint_stamp)
	docker image rm -f $(tag)
