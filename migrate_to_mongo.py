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

# ==========================================================
# 🔹 FONCTIONS 🔹
# ==========================================================

def load_csv(csv_path):
    """Lecture du CSV et affichage des infos"""
    try:
        logging.info(f"Lecture du CSV : {csv_path}")
        try:
            df = pd.read_csv(csv_path, encoding="utf-8")
        except Exception:
            df = pd.read_csv(csv_path, sep=";", encoding="utf-8")

        logging.info(f"Colonnes détectées : {list(df.columns)}")
        logging.info(f"Nombre de lignes : {len(df)}")
        logging.info("Aperçu (5 premières lignes) :\n" + df.head().to_string())

        # Conversion des dates en chaînes
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


def connect_to_mongo():
    """Connexion à MongoDB"""
    try:
        client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        logging.info(f"Connexion à MongoDB réussie : {DB_NAME}.{COLLECTION_NAME}")
        return collection
    except errors.ServerSelectionTimeoutError as e:
        logging.error(f"Impossible de se connecter à MongoDB : {e}")
        sys.exit(1)


def purge_collection(collection):
    """Vider la collection avant insertion"""
    try:
        deleted_count = collection.delete_many({}).deleted_count
        if deleted_count > 0:
            logging.info(f"Collection vidée : {deleted_count} documents supprimés.")
    except Exception as e:
        logging.error(f"Erreur lors de la purge : {e}")


def insert_data(collection, df):
    """Insérer les données dans MongoDB"""
    try:
        result = collection.insert_many(df.to_dict("records"))
        logging.info(f"{len(result.inserted_ids)} documents insérés avec succès !")
    except Exception as e:
        logging.error(f"Erreur lors de l’insertion : {e}")


def read_sample(collection):
    """Lire quelques documents pour vérification"""
    try:
        sample_docs = list(collection.find().limit(5))
        logging.info("Lecture de 5 documents :")
        for doc in sample_docs:
            logging.info(doc)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture : {e}")


def update_sample(collection, df):
    """Mettre à jour un document exemple"""
    try:
        if 'Name' in df.columns:
            update_result = collection.update_one(
                {"Name": df.loc[0, 'Name']},
                {"$set": {"Status": "Updated"}}
            )
            logging.info(f"Documents modifiés : {update_result.modified_count}")
    except Exception as e:
        logging.error(f"Erreur lors de la mise à jour : {e}")


def delete_sample(collection, df):
    """Supprimer un document exemple"""
    try:
        if 'Name' in df.columns:
            delete_result = collection.delete_one({"Name": df.loc[0, 'Name']})
            logging.info(f"Documents supprimés : {delete_result.deleted_count}")
    except Exception as e:
        logging.error(f"Erreur lors de la suppression : {e}")


def create_indexes(collection, df):
    """Créer des index pour accélérer les recherches"""
    try:
        if 'Name' in df.columns:
            collection.create_index('Name')
        if 'Date of Admission' in df.columns:
            collection.create_index('Date of Admission')
        logging.info("Index créés sur 'Name' et 'Date of Admission'.")
    except Exception as e:
        logging.error(f"Erreur lors de la création des index : {e}")


# ==========================================================
# 🔹 MAIN PROGRAM 🔹
# ==========================================================

def main():
    df = load_csv(CSV_PATH)
    collection = connect_to_mongo()

    purge_collection(collection)
    insert_data(collection, df)
    read_sample(collection)
    update_sample(collection, df)
    delete_sample(collection, df)
    create_indexes(collection, df)

    logging.info("🚀 Migration terminée avec succès !")


if __name__ == "__main__":
    main()
