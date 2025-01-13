ARG python_version
FROM python:${python_version:-3.9}-slim

ENV PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

ENV DIRPATH=/tenplatform/aiohttp-jwt
WORKDIR $DIRPATH

RUN apt-get update && \
    apt-get -qy install \
    build-essential \
    ssh


RUN mkdir -pm 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

COPY pyproject.toml poetry.lock $WORKDIR


RUN --mount=type=ssh \
    python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip  && \
    pip install poetry==1.8.* && \
    rm -r /root/.cache

# Export Poetry dependencies to `requirements.txt` for Tox environment installation.
RUN --mount=type=ssh python -m venv $VIRTUAL_ENV && poetry export --with dev --without-hashes --format=requirements.txt > requirements.txt

RUN --mount=type=ssh \
    pip install -r requirements.txt && \
    rm -r /root/.cache

COPY . $DIRPATH/

RUN ["chmod", "+x", "./ci/entrypoint.sh"]
ENTRYPOINT ["./ci/entrypoint.sh"]
