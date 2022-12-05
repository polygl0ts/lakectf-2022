FROM python:3.9-slim

RUN apt-get update && apt-get install -y gnupg && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN adduser --system --group bot

USER bot
WORKDIR /home/bot

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

COPY ./ ./

CMD ./run.sh
