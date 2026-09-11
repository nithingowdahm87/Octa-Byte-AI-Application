FROM python:3.12-alpine

# Upgrade OS packages and install build dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Run as non-root user
RUN adduser -D appuser
WORKDIR /home/appuser

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /home/appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
