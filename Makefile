name = didyouknow

.PHONY: dev docker_build docker_run

dev:
	poetry run sanic $(name):app --dev

repl:
	poetry run python3

docker_build:
	docker build --tag $(name):latest .

docker_run:
	docker run --publish 8000:8000 $(name):latest
