FROM ghcr.io/cfpb/regtech/sbl/python-alpine:3.12

ENV UVICORN_LOG_LEVEL=info

WORKDIR /usr/app

RUN pip install poetry

COPY --chown=sbl:sbl poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY --chown=sbl:sbl ./src ./src

WORKDIR /usr/app/src

EXPOSE 8765

USER sbl

CMD uvicorn regtech_mail_api.api:app --host 0.0.0.0 --port 8765 --log-config log-config.yml --log-level $UVICORN_LOG_LEVEL