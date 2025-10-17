import pandas as pd
from pymongo import MongoClient, errors
import os
import sys
import logging

# === Configuration via variables d'environnement ===
# Détection automatique :
# - Si variable MONGO_HOST est définie (ex: Docker), utilise sa valeur
# - Sinon, utilise localhost pour MongoDB local
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
DB_NAME = os.environ.get("MONGO_DB", "medical_db")
COLLECTION_NAME = os.environ.get("MONGO_COLL", "patients")

CSV_PATH = os.environ.get(
    "CSV_PATH",
    r"C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv"
)

# === Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Lecture du CSV ===
try:
    logging.info(f"Lecture du CSV : {CSV_PATH}")

    # Tentative lecture CSV avec détection du séparateur
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
    except Exception:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

    logging.info("=== Diagnostic CSV ===")
    logging.info(f"Colonnes détectées : {list(df.columns)}")
    logging.info(f"Nombre de lignes : {len(df)}")
    logging.info("Aperçu (5 premières lignes) :\n" + df.head().to_string())

    # Conversion des dates en string pour MongoDB
    for date_col in ['Date of Admission', 'Discharge Date']:
        if date_col in df.columns:
            df[date_col] = df[date_col].astype(str)

except Exception as e:
    logging.error(f"Impossible de lire le CSV : {e}")
    sys.exit(1)

if len(df) == 0:
    logging.warning("Le fichier CSV est vide. Vérifie le séparateur ou le chemin.")
    sys.exit(1)

# === Connexion à MongoDB ===
try:
    client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')  # Test de connexion
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logging.info(f"Connexion à MongoDB réussie : {DB_NAME}.{COLLECTION_NAME}")
except errors.ServerSelectionTimeoutError as e:
    logging.error(f"Impossible de se connecter à MongoDB : {e}")
    sys.exit(1)

# === Optionnel : vider la collection avant insertion ===
try:
    deleted_count = collection.delete_many({}).deleted_count
    if deleted_count > 0:
        logging.info(f"Collection vidée : {deleted_count} documents supprimés.")
except Exception as e:
    logging.error(f"Erreur lors de la purge de la collection : {e}")

# === Insertion des données ===
try:
    result = collection.insert_many(df.to_dict("records"))
    logging.info(f"Migration terminée avec succès ! {len(result.inserted_ids)} documents insérés.")

    # Création d'index
    if 'Name' in df.columns:
        collection.create_index('Name')
    if 'Date of Admission' in df.columns:
        collection.create_index('Date of Admission')
    logging.info("Index créés sur 'Name' et 'Date of Admission'.")
except Exception as e:
    logging.error(f"Erreur lors de l’insertion : {e}")
