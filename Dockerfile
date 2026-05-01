FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DEBUG=False SECRET_KEY=build-only python manage.py collectstatic --noinput --clear

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py ensure_superuser && exec gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --worker-class sync --timeout 120 --access-logfile - --error-logfile - --log-level info"]
