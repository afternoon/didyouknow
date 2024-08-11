name = didyouknow
tag = $(name):latest

.PHONY: dev docker_build docker_run

dev:
	poetry run sanic $(name):app --dev

repl:
	poetry run python3

docker_build: Dockerfile didyouknow/*.py
	docker build --tag $(tag) .

docker_run:
	docker run --publish 8000:8000 $(tag)
