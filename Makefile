-include .env
export

runserver:
	@poetry run python src/manage.py runserver
