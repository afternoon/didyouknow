name = didyouknow

.PHONY: dev docker_build docker_run

dev:
	poetry run python3 $(name)/__main__.py

repl:
	poetry run python3

docker_build:
	docker build --tag $(name):latest .

docker_run:
	docker run --publish 8000:8000 $(name):latest
