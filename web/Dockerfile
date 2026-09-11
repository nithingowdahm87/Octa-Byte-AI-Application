FROM python:3.12-alpine

# Upgrade OS packages and install build dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Run as non-root user
RUN adduser -D appuser
WORKDIR /home/appuser

COPY requirements.txt requirements.txt

# Create venv and install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools && \
    /venv/bin/pip install -r requirements.txt

# Remove system-level setuptools, pip, and msgpack to silence Trivy false positives on the base image
RUN rm -rf /usr/local/lib/python3.12/site-packages/setuptools* \
           /usr/local/lib/python3.12/site-packages/pip* \
           /usr/local/lib/python3.12/site-packages/msgpack* \
           /usr/local/lib/python3.12/ensurepip

COPY . .

RUN chown -R appuser:appuser /home/appuser /venv
USER appuser
ENV PATH="/venv/bin:$PATH"

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
