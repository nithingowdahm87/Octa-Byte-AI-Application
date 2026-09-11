FROM python:3.10

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

COPY . .CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
