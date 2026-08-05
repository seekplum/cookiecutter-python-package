FROM python:3.13-slim-bookworm AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM base AS compile-stage

WORKDIR /code

ADD pyproject.toml uv.lock README.md .

ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Shanghai

RUN set -xe && \
    unlink /etc/localtime && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone && \
    sed -i 's#http://\(security\|deb\).debian.org#https://mirrors.aliyun.com#g' /etc/apt/sources.list.d/debian.sources && \
    uv sync --no-dev --frozen

FROM compile-stage AS runtime-stage

WORKDIR /code

ADD src ./src

ARG BUILD_ID
ARG BUILD_VERSION
ENV BUILD_ID=${BUILD_ID}
ENV BUILD_VERSION=${BUILD_VERSION}

ENV PATH="/code/.venv/bin:${PATH}"
ENV PYTHONPATH="/code"
