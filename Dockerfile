FROM 133824686826.dkr.ecr.eu-west-1.amazonaws.com/docker-hub/library/debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /var/aiohttp-jwt/
ARG PYTHON_VERSIONS="3.10 3.11 3.12"

# Install dependencies.
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    git \
    ca-certificates \
    libffi-dev \
    ssh \
    libpq-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    liblzma-dev \
    && apt-get clean autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /var/cache/apt/archives/*.deb

# Install ``pyenv``.
RUN git clone https://github.com/pyenv/pyenv /root/.pyenv

# Install the desired versions of Python.
RUN for PYTHON_VERSION in ${PYTHON_VERSIONS}; do \
    set -ex \
    && /root/.pyenv/bin/pyenv install ${PYTHON_VERSION} \
    ; done

# Add Python versions to PATH.
RUN for PYTHON_VERSION in $(ls /root/.pyenv/versions); do \
    set -ex \
    && PYENV_BIN_PATH="/root/.pyenv/versions/${PYTHON_VERSION}/bin" \
    && echo 'export PATH="'${PYENV_BIN_PATH}':$PATH"' >> /root/.bash_profile \
    ; done

# Set the default Python version.
RUN set -ex \
    && FIRST_VERSION=$(echo ${PYTHON_VERSIONS} | awk '{print $1}') \
    && echo "alias python=python${FIRST_VERSION}" >> /root/.bash_profile

# Upgrade pip for all Python versions.
RUN for PYTHON_VERSION in ${PYTHON_VERSIONS}; do \
    set -ex \
    && /bin/bash -l -c "python${PYTHON_VERSION} -m pip install --upgrade pip" \
    ; done

# Copy dependencies
COPY pyproject.toml poetry.lock ./

# Install Poetry and Tox.
RUN /bin/bash -l -c "python -m pip install --upgrade pip \
    && pip install poetry==1.4.* \
    && pip install tox==$(grep -A 1 'name = \"tox\"' poetry.lock | grep 'version = ' | awk -F'\"' '{print \$2}')"

# Export Poetry dependencies to `requirements.txt` for Tox environment installation.
RUN /bin/bash -l -c "poetry export --with dev --without-hashes --format=requirements.txt > requirements.txt"

# Copy the files needed to install tox environments.
COPY setup.cfg setup.py README.md ./
RUN mkdir ./aiohttp_jwt
COPY aiohttp_jwt/__init__.py ./aiohttp_jwt/__init__.py

# Install tox environments.
RUN /bin/bash -l -c "python -m tox run --notest"

# Copy entrypoint script
COPY ci/entrypoint.sh ./ci/entrypoint.sh

RUN ["chmod", "+x", "./ci/entrypoint.sh"]
ENTRYPOINT ["./ci/entrypoint.sh"]
