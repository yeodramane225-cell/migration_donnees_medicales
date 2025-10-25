import pandas as pd
from pymongo import MongoClient, errors
import os
import sys
import logging
from dotenv import load_dotenv
import socket
import time

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configuration via variables d'environnement
DB_NAME = os.environ.get("MONGO_DB", "medical_db")
COLLECTION_NAME = os.environ.get("MONGO_COLL", "patients")
MONGO_USER = os.environ.get("MONGO_MIGRATION_USER")
MONGO_PASS = os.environ.get("MONGO_MIGRATION_PASS")
AUTH_DB = os.environ.get("MONGO_AUTH_DB", DB_NAME)  # Auth sur la même base ou admin

# Hosts et ports à tester (local et Docker)
MONGO_HOSTS = {
    "local": {
        "host": os.environ.get("MONGO_LOCAL_HOST", "localhost"),
        "port": int(os.environ.get("MONGO_LOCAL_PORT", 27017))
    },
    "docker": {
        "host": os.environ.get("MONGO_DOCKER_HOST", "mongo_medical"),
        "port": int(os.environ.get("MONGO_DOCKER_PORT", 27017))
    }
}

# Chemin du CSV
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.environ.get(
    "CSV_PATH",
    os.path.normpath(os.path.join(BASE_DIR, "..", "dataset", "healthcare_dataset.csv"))
)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ==========================================================
# FONCTIONS CSV
# ==========================================================
def load_csv(csv_path):
    if not os.path.exists(csv_path):
        logging.error(f"Le fichier CSV n'existe pas : {csv_path}")
        sys.exit(1)
    try:
        logging.info(f"Lecture du CSV : {csv_path}")
        try:
            df = pd.read_csv(csv_path, encoding="utf-8")
        except Exception:
            df = pd.read_csv(csv_path, sep=";", encoding="utf-8")

        logging.info(f"Colonnes détectées : {list(df.columns)}")
        logging.info(f"Nombre de lignes : {len(df)}")
        logging.info("Aperçu (5 premières lignes) :\n" + df.head().to_string())

        # Conversion des colonnes de dates en chaînes
        for date_col in ['Date of Admission', 'Discharge Date']:
            if date_col in df.columns:
                df[date_col] = df[date_col].astype(str)

        if len(df) == 0:
            logging.warning("Le fichier CSV est vide.")
            sys.exit(1)
        return df
    except Exception as e:
        logging.error(f"Impossible de lire le CSV : {e}")
        sys.exit(1)

# ==========================================================
# FONCTIONS RESEAU
# ==========================================================
def is_host_reachable(host, port):
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except Exception:
        return False

def wait_for_host(host, port, retries=10, delay=2):
    for attempt in range(1, retries + 1):
        if is_host_reachable(host, port):
            return True
        logging.info(f"Attente de {host}:{port} (tentative {attempt}/{retries})...")
        time.sleep(delay)
    logging.warning(f"{host}:{port} inaccessible après {retries} tentatives.")
    return False

# ==========================================================
# FONCTION DE CONNEXION
# ==========================================================
def connect_to_mongo(host, port):
    try:
        client = MongoClient(
            f"mongodb://{MONGO_USER}:{MONGO_PASS}@{host}:{port}/{DB_NAME}?authSource={AUTH_DB}",
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        logging.info(f"Connexion réussie à {host}:{port} → {DB_NAME}.{COLLECTION_NAME}")
        return collection
    except errors.ServerSelectionTimeoutError as e:
        logging.error(f"Impossible de se connecter à MongoDB ({host}:{port}): {e}")
    except errors.OperationFailure as e:
        logging.error(f"Erreur d'authentification sur {host}:{port}: {e}")
    return None

# ==========================================================
# CRUD COMPLET
# ==========================================================
def create_documents(collection, data):
    try:
        result = collection.insert_many(data)
        logging.info(f"{len(result.inserted_ids)} documents créés avec succès.")
    except Exception as e:
        logging.error(f"Erreur lors de la création : {e}")

def read_documents(collection, query={}, limit=5):
    try:
        docs = list(collection.find(query).limit(limit))
        logging.info(f"Lecture {len(docs)} documents :\n{docs}")
        return docs
    except Exception as e:
        logging.error(f"Erreur lors de la lecture : {e}")
        return []

def update_documents(collection, query, update):
    try:
        result = collection.update_many(query, {"$set": update})
        logging.info(f"{result.modified_count} documents mis à jour.")
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour : {e}")

def delete_documents(collection, query={}):
    try:
        result = collection.delete_many(query)
        logging.info(f"{result.deleted_count} documents supprimés.")
    except Exception as e:
        logging.error(f"Erreur lors de la suppression : {e}")

# ==========================================================
# MIGRATION
# ==========================================================
def migrate_to_collection(collection, df, host_name):
    if collection is None:
        logging.warning(f"Migration ignorée pour {host_name} (collection non disponible).")
        return
    try:
        delete_documents(collection)  # Purge
        create_documents(collection, df.to_dict("records"))  # Insertion
        if 'Name' in df.columns:
            collection.create_index('Name')
        if 'Date of Admission' in df.columns:
            collection.create_index('Date of Admission')
        logging.info(f"[{host_name}] Index créés sur 'Name' et 'Date of Admission'.")
    except Exception as e:
        logging.error(f"Erreur lors de la migration sur {host_name}: {e}")

# ==========================================================
# MAIN PROGRAM
# ==========================================================
def main():
    df = load_csv(CSV_PATH)

    for host_name, host_info in MONGO_HOSTS.items():
        host = host_info["host"]
        port = host_info["port"]
        logging.info(f"Tentative de connexion à {host_name} ({host}:{port})")
        if wait_for_host(host, port):
            collection = connect_to_mongo(host, port)
            migrate_to_collection(collection, df, host_name)
        else:
            logging.warning(f"{host_name} ({host}:{port}) inaccessible, migration ignorée.")

    logging.info("Migration terminée sur toutes les bases accessibles.")

if __name__ == "__main__":
    main()
