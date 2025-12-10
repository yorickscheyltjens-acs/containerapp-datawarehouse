# ---- Base image ----
FROM python:3.11-slim

# Snellere/duidelijkere runtime
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=Europe/Brussels

# Werkdirectory in de container
WORKDIR /app

# 1) Dependencies eerst (betere build cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Applicatiecode
COPY app/ ./app

# 3) Niet-root gebruiker (veiliger in productie)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# 4) Start als Python package → stabiele imports vanuit /app
CMD ["python", "-m", "app.main"]
