FROM python:3.10.2-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /webapp

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /webapp/
RUN poetry install --no-dev

COPY src /webapp/src

#RUN cd src/

#CMD python src/manage.py runserver 0.0.0.0

#CMD ["python", "-m", "src/manage.py", "runserver", "0.0.0.0:8000"]