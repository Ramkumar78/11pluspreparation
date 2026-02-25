FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with ownership
COPY --chown=appuser:appuser . .

# Ensure the working directory is owned by the user (non-recursive to avoid layer bloat, files are already owned)
RUN chown appuser:appuser /app

# Switch to the non-root user
USER appuser

CMD ["sh", "-c", "python -c 'from seeder import init_db; from app import app; ctx=app.app_context(); ctx.push(); init_db()' && gunicorn --bind 0.0.0.0:5001 wsgi:app"]
