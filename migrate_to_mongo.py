import pandas as pd
from pymongo import MongoClient, errors
import os
import sys
import logging

# === Configuration via variables d'environnement ===
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
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8")
    except Exception:
        df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

    logging.info(f"Colonnes détectées : {list(df.columns)}")
    logging.info(f"Nombre de lignes : {len(df)}")
    logging.info("Aperçu (5 premières lignes) :\n" + df.head().to_string())

    for date_col in ['Date of Admission', 'Discharge Date']:
        if date_col in df.columns:
            df[date_col] = df[date_col].astype(str)
except Exception as e:
    logging.error(f"Impossible de lire le CSV : {e}")
    sys.exit(1)

if len(df) == 0:
    logging.warning("Le fichier CSV est vide.")
    sys.exit(1)

# === Connexion à MongoDB ===
try:
    client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logging.info(f"Connexion à MongoDB réussie : {DB_NAME}.{COLLECTION_NAME}")
except errors.ServerSelectionTimeoutError as e:
    logging.error(f"Impossible de se connecter à MongoDB : {e}")
    sys.exit(1)

# === DELETE (vider la collection avant insertion) ===
try:
    deleted_count = collection.delete_many({}).deleted_count
    if deleted_count > 0:
        logging.info(f"Collection vidée : {deleted_count} documents supprimés.")
except Exception as e:
    logging.error(f"Erreur lors de la purge : {e}")

# === CREATE (Insertion des données) ===
try:
    result = collection.insert_many(df.to_dict("records"))
    logging.info(f"{len(result.inserted_ids)} documents insérés avec succès !")
except Exception as e:
    logging.error(f"Erreur lors de l’insertion : {e}")

# === READ (lecture de 5 documents) ===
try:
    sample_docs = list(collection.find().limit(5))
    logging.info("Lecture de 5 documents :")
    for doc in sample_docs:
        logging.info(doc)
except Exception as e:
    logging.error(f"Erreur lors de la lecture : {e}")

# === UPDATE (mise à jour d'un document exemple) ===
try:
    if 'Name' in df.columns:
        update_result = collection.update_one(
            {"Name": df.loc[0, 'Name']},
            {"$set": {"Status": "Updated"}}
        )
        logging.info(f"Documents modifiés : {update_result.modified_count}")
except Exception as e:
    logging.error(f"Erreur lors de la mise à jour : {e}")

# === DELETE (suppression d'un document exemple) ===
try:
    if 'Name' in df.columns:
        delete_result = collection.delete_one({"Name": df.loc[0, 'Name']})
        logging.info(f"Documents supprimés : {delete_result.deleted_count}")
except Exception as e:
    logging.error(f"Erreur lors de la suppression : {e}")

# === Création d'index ===
try:
    if 'Name' in df.columns:
        collection.create_index('Name')
    if 'Date of Admission' in df.columns:
        collection.create_index('Date of Admission')
    logging.info("Index créés sur 'Name' et 'Date of Admission'.")
except Exception as e:
    logging.error(f"Erreur lors de la création des index : {e}")
