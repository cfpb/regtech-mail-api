FROM python:3.12-alpine

WORKDIR /usr/app/src

RUN pip install poetry

COPY poetry.lock pyproject.toml log-config.yml ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY src/ ./

EXPOSE 8765

CMD ["uvicorn", "regtech_mail_api.api:app", "--host", "0.0.0.0", "--port", "8765", "--log-config", "log-config.yml"]
