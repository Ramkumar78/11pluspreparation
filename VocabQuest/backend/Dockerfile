FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python -c 'from seeder import init_db; from app import app; ctx=app.app_context(); ctx.push(); init_db()' && gunicorn --bind 0.0.0.0:5001 wsgi:app"]
