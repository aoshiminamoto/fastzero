FROM python:3.12-slim

ENV TIMEZONE=Brazil/East
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . /app

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD ["uvicorn", "fastzero.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
