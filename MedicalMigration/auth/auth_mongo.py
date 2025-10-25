import os
from pymongo import MongoClient
import logging
from dotenv import load_dotenv

# === Charger les variables d'environnement depuis un fichier .env si présent ===
load_dotenv()

# === Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Récupération des credentials depuis variables d'environnement ===
try:
    ADMIN_USER = os.environ["MONGO_ADMIN_USER"]
    ADMIN_PASS = os.environ["MONGO_ADMIN_PASS"]
    MIGRATION_USER = os.environ["MONGO_MIGRATION_USER"]
    MIGRATION_PASS = os.environ["MONGO_MIGRATION_PASS"]
    READ_USER = os.environ["MONGO_READ_USER"]
    READ_PASS = os.environ["MONGO_READ_PASS"]
except KeyError as e:
    logging.error(f"Variable d'environnement manquante : {e}")
    exit(1)

# === Connexion au serveur MongoDB avec admin pour pouvoir créer des utilisateurs ===
client = MongoClient(f"mongodb://{ADMIN_USER}:{ADMIN_PASS}@localhost:27017/admin")

def create_user_if_not_exists(db_name, username, password, roles):
    db = client.get_database(db_name)
    try:
        existing_users = [user["user"] for user in db.command("usersInfo")["users"]]
        if username in existing_users:
            logging.info(f"Utilisateur '{username}' existe déjà dans la DB '{db_name}'.")
            return
        db.command(
            "createUser",
            username,
            pwd=password,
            roles=roles
        )
        logging.info(f"Utilisateur '{username}' créé avec succès dans la DB '{db_name}'.")
    except Exception as e:
        logging.warning(f"Erreur création utilisateur '{username}': {e}")

if __name__ == "__main__":
    # Créer les utilisateurs si nécessaire
    create_user_if_not_exists("admin", ADMIN_USER, ADMIN_PASS, [{"role": "userAdminAnyDatabase", "db": "admin"}])
    create_user_if_not_exists("MedicalMigration", MIGRATION_USER, MIGRATION_PASS, [{"role": "readWrite", "db": "MedicalMigration"}])
    create_user_if_not_exists("MedicalMigration", READ_USER, READ_PASS, [{"role": "read", "db": "MedicalMigration"}])
    logging.info("Vérification/création des utilisateurs terminée !")
