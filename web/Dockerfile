FROM python:3.10-slim

# Upgrade OS packages to patch known CVEs
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Run as non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /home/appuser
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
