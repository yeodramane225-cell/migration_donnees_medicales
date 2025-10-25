FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY MedicalMigration/scripts/ ./scripts/
COPY MedicalMigration/dataset/ ./dataset/
COPY MedicalMigration/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scripts/mongo_migration.py"]
