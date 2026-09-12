# ---------- Builder stage ----------
FROM python:3.12-alpine AS builder

RUN apk update && apk upgrade && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

WORKDIR /build

COPY requirements.txt requirements.txt

ENV PIP_NO_CACHE_DIR=1

# Create venv, upgrade pip/setuptools to patched versions, install deps.
# Pinning setuptools/msgpack floors here guards against any transitive
# build-time resolution pulling a vulnerable version.
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir --upgrade "pip>=24" "setuptools>=78.1.1" && \
    /venv/bin/pip install --no-cache-dir "msgpack>=1.2.1" && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

# Belt-and-braces: purge any pip cache/build leftovers before the copy.
RUN rm -rf /root/.cache/pip /root/.cache/* /tmp/*

# ---------- Final stage ----------
FROM python:3.12-alpine

RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache libpq

RUN adduser -D appuser
WORKDIR /home/appuser

# Only the clean venv is brought over -- no build tools, no pip cache,
# no leftover wheels from the builder stage.
COPY --from=builder /venv /venv

COPY . .

RUN chown -R appuser:appuser /home/appuser /venv
USER appuser
ENV PATH="/venv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]