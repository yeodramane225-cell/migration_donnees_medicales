# Migration des Données Médicales vers MongoDB avec Docker

![migration_des_donnees](https://github.com/user-attachments/assets/4caec7d1-9d12-41ef-a7f4-380f393cf52e)

```
Sommaire
Contexte du projet

Présentation du stage et de l’entreprise DataSoluTech

Objectifs principaux du projet

Architecture cible et technologies utilisées

Livrables attendus

Préparation de l’environnement

Prérequis techniques

Outils à installer

Structure initiale du projet

Arborescence détaillée des fichiers

Analyse et traitement du dataset médical

Chargement et exploration du fichier healthcare_dataset.csv

Description des colonnes et types de données

Gestion des doublons et valeurs manquantes

Nettoyage et préparation des données

Mise en place de MongoDB conteneurisé

Création du dossier docker/ et du fichier docker-compose.yml

Lancement de MongoDB avec Docker Compose

Vérification du conteneur et test de connexion

Identification de l’adresse IP du conteneur

Développement du script de migration Python

Création de l’environnement virtuel et installation des dépendances

Fichier requirements.txt

Développement du script migrate_to_mongo.py

Test local de la migration

Connexion à MongoDB et insertion des données

Gestion des erreurs et création d’index

Conteneurisation complète de la solution

Structure finale du projet

Création du Dockerfile

Configuration du docker-compose.yml

Construction et exécution des conteneurs

Vérification et validation de la migration

Visualisation des données dans MongoDB

Débogage et résolution d’erreurs

Erreur d’incompatibilité entre Pandas et NumPy

Vérification des logs Docker

Ajustement des dépendances dans requirements.txt

Reconstruction des conteneurs et test final

Résultats finaux

Données migrées avec succès (≈ 55 500 documents insérés)

Index créés dans MongoDB

Conteneurs fonctionnels et persistants

Architecture finale validée

Documentation — Passage au cloud AWS

Création d’un compte AWS

Compréhension de la tarification AWS

Solutions AWS compatibles MongoDB :

Amazon DocumentDB

MongoDB conteneurisé sur Amazon ECS

Étapes de déploiement sur ECS

Liens et ressources officielles AWS

Étapes pratiques d’exploration via la console AWS

Conclusion

Bilan du projet et compétences acquises

Avantages de la solution conteneurisée

Perspectives d’évolution (intégration AWS, automatisation CI/CD, scalabilité)
```

## Contexte

Je suis stagiaire Data Engineer chez DataSoluTech, sous la supervision de Boris.
Le client dispose d’un dataset médical volumineux et rencontre des problèmes de scalabilité avec ses traitements actuels.

L’objectif du projet est triple :

**Migrer les données issues d’un fichier CSV vers MongoDB**

**Conteneuriser la solution avec Docker et Docker Compose**

**Préparer la migration future vers AWS pour un déploiement cloud scalable et automatisé**

Le déploiement repose sur deux conteneurs :

**MongoDB** : base de données NoSQL pour stocker les informations des patients.
**Python Migration** : script Python qui lit le CSV et insère les données dans MongoDB.



## Étape 0 : création de branche pour la bonne gestion du projet dans git(github)

## Création des autres branches, script et test (prioriser de travailler sur les autres branche avant de fusionner les modifications ou le travail sur la branche principale(main) (dans mon cas les autres branches ont été crées après et les modifications reportées sur la branche main(maître), mais le projet avait été deployé sur la branche main)


```
                             ┌──────────────────────────────────┐
                             │         MAIN (branche stable)    │
                             │----------------------------------│
                             │Contient la version validée du    │
                             │projet après fusion CI/CD.        │
                             │Déploie la migration complète.    │
                             └───────────────┬──────────────────┘
                                             │
           ┌────────────────────────────────┴────────────────────────────────┐
           │                                                                 │
┌──────────────────────────────────┐                         ┌──────────────────────────────────┐
│ feature/tests-unitaires          │                         │ feature/authentification         │
│----------------------------------│                         │----------------------------------│
│    Objectif :                    │                         │    Objectif :                    │
│ Tester le script de migration et │                         │ Créer les utilisateurs MongoDB   │
│ la structure de la base Mongo.   │                         │ (admin, migration, read-only).   │
│----------------------------------│                         │----------------------------------│
│    Contient : test_migration.py  │                         │    Contient : auth_mongo.py      │
│----------------------------------│                         │----------------------------------│
│    Commandes clés :              │                         │    Commandes clés :              │
│  - python -m unittest discover   │                         │  - python auth/auth_mongo.py     │
│  - git push origin feature/...   │                         │  - mongosh pour vérifier users   │
└──────────────────────────────────┘                         └──────────────────────────────────┘
           │                                                                 │
           ├────────────────────────────────┬────────────────────────────────┤
           │                                │                                │
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│ feature/analyse-donnees          │  │ feature/configuration-docker     │
│----------------------------------│  │----------------------------------│
│ Objectif :                    │  │       Objectif :                    │
│ Nettoyer et analyser les données │  │ Conteneuriser le projet avec     │
│ avant migration vers MongoDB.    │  │ MongoDB et Python.               │
│----------------------------------│  │----------------------------------│
│ Contient : data_cleaning.py   │  │      Contient : Dockerfile +        │
│                                  │  │              docker-compose.yml  │
│----------------------------------│  │----------------------------------│
│    Commandes clés :              │  │    Commandes clés :              │
│  - python scripts/data_cleaning  │  │  - docker-compose up --build     │
│  - git push origin feature/...   │  │  - test conteneur Mongo actif    │
└──────────────────────────────────┘  └──────────────────────────────────┘
```
 branche principal(maître) :main : branche existant 
feature/tests-unitaires

feature/authentification

feature/analyse-donnees

feature/configuration-docker


## Étape 1 : Préparation

Prérequis :

**Avoir consulté les ressources sur le NoSQL et Docker** **Cours OpenClassrooms – Optimisez votre déploiement en créant des conteneurs avec Docker**

Installer sur Mon poste :

**Docker Desktop + Docker Compose**

**Python 3 + pip**

**Git**

**VS Code ou autre éditeur de code**

Livrables à produire :

**Script Python pour la migration.**

**docker-compose.yml pour MongoDB et le script.**

**README détaillé pour expliquer la migration.**

**requirements.txt pour ton environnement Python.**

**Présentation finale (PowerPoint ou autre).**


## Étape 2 : Structure du projet

Crée un dossier projet Migration_donnees_medicales :

## Arborescence du projet

```
Migration_donnees_medicales/
│
├─ MedicalMigration/
│  ├─ scripts/
│  │  ├─ migrate_to_mongo.py        # script principal de migration (CRUD complet)
│  │  ├─ data_cleaning.py           # pré-traitement du dataset
│  │  ├─ mongo_migration.py         # fonctions MongoDB supplémentaires (si nécessaire)
│  │  └─ __pycache__/               # fichiers compilés Python
│  │
│  ├─ auth/
│  │  └─ auth_mongo.py              # gestion des utilisateurs MongoDB
│  │
│  ├─ dataset/
│  │  └─ healthcare_dataset.csv     # dataset médical source
│  │
│  ├─ __init__.py                   # rendre MedicalMigration un package Python
│  ├─ requirements.txt              # dépendances Python
│  └─ .github/
│     └─ workflows/
│        └─ ci_cd.yml               # pipeline CI/CD GitHub Actions
│
├─ docker/
│  ├─ Dockerfile                     # image Python + MongoDB client
│  └─ docker-compose.yml             # orchestration MongoDB + app
│
├─ schema/
│  └─ medical_db.patients.json       # schéma JSON de la base MongoDB
│
├─ tests/
│  ├─ test_migration.py              # tests unitaires pour migrate_to_mongo.py
│  └─ __pycache__/                   # fichiers compilés Python
│
├─ .env                              # variables d’environnement (MongoDB URI, credentials)
├─ README.md                          # documentation principale du projet
└─ .gitignore                         # fichiers à ne pas pousser (logs, CSV, venv, etc.)



```
## Etape 3 : analyse et traitement de healthcare_dataset.csv
## création de script python d'analyse (le script donne le nombre d'enregistrement ou document, le nom des colonnes, les variables,les doublons ...) 
## script : data_cleaning.py
```
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)

def analyze_dataset(file_path):
    # Lecture du CSV
    df = pd.read_csv(file_path)
    
    # Nombre de lignes et colonnes
    total_rows = len(df)
    total_columns = len(df.columns)
    column_names = list(df.columns)
    
    # Nombre de doublons
    duplicate_rows = df.duplicated().sum()
    
    logging.info(f"Nombre total de lignes : {total_rows}")
    logging.info(f"Nombre total de colonnes : {total_columns}")
    logging.info(f"Colonnes : {column_names}")
    logging.info(f"Nombre de doublons : {duplicate_rows}")
    
    # Optionnel : aperçu des doublons
    if duplicate_rows > 0:
        logging.info(f"Exemple de doublons :\n{df[df.duplicated()].head()}")

if __name__ == "__main__":
    # Chemin absolu du CSV, indépendant du dossier courant
    base_dir = os.path.dirname(__file__)  # répertoire du script
    csv_path = os.path.abspath(os.path.join(base_dir, "..", "dataset", "healthcare_dataset.csv"))

    analyze_dataset(csv_path)


```

## Étape 4 : MongoDB en local
### installation de mongoDB en local (sur Windows, sur Linux (VM), MongoDB compass)
### Création du script python de migration : mongo_migration.py
### Authentification (création des utilisateurs (admin ,minimum) et rôles avant migration) Ou le faire lors de l'étape de conténarisation
### migration des données dans mongoDB en local (vérification des collections, des enregistrement après migration)
### (présence des fonction crud (delete, create, update, read)
### script python de migration:mongo_migration.py:

```
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

```


## Étape 5 : MongoDB conteneurisé
### Créer l’arborescence du projet

Dans ton projet, crée un dossier docker :

```
mkdir docker cd docker
```

Puis, crée le fichier docker-compose.yml :

Utiliser le Bloc-notes

--Dans PowerShell :
```
notepad docker-compose.yml
```

Si le fichier n’existe pas, il demandera de le créer.

Coller ensuite ton contenu YAML et enregistre.

--Utiliser Visual Studio Code (si installé)

Si tu as VS Code :

```
code docker-compose.yml
```

Cela ouvrira le fichier dans VS Code.

Tu peux le modifier et sauvegarder directement.

--dans linux nano docker-compose.yml

Copie-colle le contenu suivant :

```
version: '3.8'

services: mongo: image: mongo:latest container_name: medical_mongo ports: - "27017:27017" volumes: - mongo_data:/data/db

volumes: mongo_data:

```

Enregistre et ferme le fichier.

## Lancer MongoDB avec Docker Compose

s'assurer qu'on est dans le dossier docker où se trouve docker-compose.yml puis exécute :

```
docker-compose up -d
```

L’option -d lance le conteneur en arrière-plan (détaché).

Docker va télécharger l’image officielle mongo:latest si elle n’existe pas encore.

## Vérifier que le conteneur tourne

Pour voir les conteneurs en cours d’exécution :
```
docker ps
```

Tu devrais voir quelque chose comme :

CONTAINER ID IMAGE COMMAND STATUS PORTS NAMES abcd1234 mongo:latest "docker-entrypoint.s…" Up 10s 0.0.0.0:27017->27017/tcp medical_mongo

STATUS: Up → MongoDB fonctionne.

PORTS: 27017 → tu peux te connecter à MongoDB depuis ton script Python ou Mongo Shell sur ce port.

## Tester la connexion à MongoDB (optionnel)

--on peut aller dans le shell de mongodb depuis le contenaire et fait : mongosh

on verra normalement mongodb se connecter (base test apparait)

--on peut aussi depuis vscode : aller dans le dossier (exemeple cd : C:\Users\yeodr\Migration_donnees_medicales\docker) et fait : docker exec -it medical_mongo mongosh

--Si tu as installé pymongo en Python :
```
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") db = client.test_db print(db.list_collection_names())

```

Tu devrais voir une liste vide pour l’instant, car aucune collection n’est encore créée.


## Étape 6 : Modification du Script Python de migration vers MongoDB pour migration des données en local et dans le conteneur docker
### Créer l’environnement virtuel Python

Ouvre PowerShell et place-toi dans le dossier du projet :
```
cd C:\Users\yeodr\Migration_donnees_medicales

```

### Crée un environnement virtuel appelé venv :
```
python -m venv venv
```

### Active l’environnement virtuel :
```
.\venv\Scripts\Activate.ps1
```

Tu devrais voir (venv) au début de la ligne PowerShell. Cela signifie que tu es dans un environnement Python isolé.

### Optionnel : mets à jour pip :
```
python -m pip install --upgrade pip
```

## Installer les dépendances Python

### Crée un dossier scripts dans ton projet si ce n’est pas déjà fait :
```
mkdir .\MedicalMigration\scripts
```

### Crée le fichier requirements.txt dans ce dossier :
```
notepad .\MedicalMigration\scripts\requirements.txt
```

Copie-colle dedans :
```
pandas pymongo

Installe les modules dans l’environnement virtuel :

pip install -r .\MedicalMigration\scripts\requirements.txt
```

À ce stade, ton environnement virtuel est prêt avec pandas et pymongo installés.


### Modifié le fichier migrate_to_mongo.py dans le dossier scripts :
```
notepad .\MedicalMigration\scripts\migrate_to_mongo.py
```

### Authentifications (création d'utilisateur et rôle)
### fichiers crées : auth_mongo.py, .env
### auth_mongo.py (script de création des utilisateurs)
### .env (script pour stocker les mots de passes pour des raisons sécuritaires, n'est pas exposé en public sur github)
### .gitignore (pour ignorer les mots de passes pour ne pas qu'ils soient présent en public sur gitHub)
### création de 3 utilisateurs (admin_user, read_user, migration_user)

```

\033[32m
                              ┌──────────────────────────────┐
                              │        Admin (admin_user)    │
                              │------------------------------│
                              │ Rôle : root                  │
                              │ Accès : bases medical_db,    │
                              │          MedicalMigration    │
                              │ Auth DB : medical_db ou      │
                              │           MedicalMigration   │
                              │ Connexion :                  │
                              │ mongosh -u admin_user -p password │
                              │   --authenticationDatabase medical_db │
                              └──────────────┬───────────────┘
                                             │
           ┌────────────────────────────────┴────────────────────────────────┐
           │                                                                 │
┌──────────────────────────────┐                         ┌──────────────────────────────┐
│ Migration (migration_user)   │                         │ Lecture seule (read_user)   │
│------------------------------│                         │-----------------------------│
│ Rôle : readWrite             │                         │ Rôle : read                 │
│ Accès : bases medical_db,    │                         │ Accès : bases medical_db,   │
│          MedicalMigration    │                         │          MedicalMigration   │
│ Auth DB : medical_db ou      │                         │ Auth DB : medical_db ou     │
│           MedicalMigration   │                         │           MedicalMigration  │
│ Connexion :                  │                         │ Connexion :                 │
│ mongosh -u migration_user -p password │                │ mongosh -u read_user -p password │
│   --authenticationDatabase medical_db │                │   --authenticationDatabase medical_db │
│ Peut : insert / update / delete │                      │ Peut : uniquement find()    │
│ Ne peut pas : créer d’utilisateurs │                   │ Ne peut pas : écrire        │
└──────────────────────────────┘                         └─────────────────────────────┘

```


Ran 2 tests in X.XXXs
OK

➤ Étape 4 — Commit & Push
git add .
git commit -m "Ajout des tests unitaires du script de migration"
git push origin feature/tests-unitaires

B. Branche : feature/authentification
➤ Étape 1 — Retour à main et création
git checkout main
git pull origin main
git checkout -b feature/authentification

➤ Étape 2 — Créer le répertoire et le fichier
mkdir MedicalMigration\auth
notepad MedicalMigration\auth\auth_mongo.py


### script : auth_mongo.py

Colle le script 


```
import os
from pymongo import MongoClient
import logging

# === Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# === Récupération des credentials depuis variables d'environnement ===
ADMIN_USER = os.environ.get("MONGO_ADMIN_USER", "admin_user")
ADMIN_PASS = os.environ.get("MONGO_ADMIN_PASS", "securePass123")

MIGRATION_USER = os.environ.get("MONGO_MIGRATION_USER", "migration_user")
MIGRATION_PASS = os.environ.get("MONGO_MIGRATION_PASS", "migrationPass!")

READ_USER = os.environ.get("MONGO_READ_USER", "read_user")
READ_PASS = os.environ.get("MONGO_READ_PASS", "readonly123")

# === Connexion au serveur MongoDB ===
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

```

### Deux manières de créer les utilisateurs et les roles: soit en exécutant le script (d'abord lancé mongodb en mode sans authentification avant de lancer le script
et après l'exécution du script, lancé mondb avec le mode authentification et essayé de se connecter puis exécuté le script de migration)
soit en se connectant à mongodb directement et créer les utilisateurs et rôle manuellement

>>Se connecte au serveur MongoDB local.

Crée trois utilisateurs avec des rôles différents :

admin_user → administrateur capable de gérer toutes les bases et utilisateurs.

migration_user → peut lire et écrire dans la base MedicalMigration.

read_user → peut seulement lire les données dans la base MedicalMigration.

Utilise les mots de passe définis dans les variables d’environnement.

Affiche des logs pour confirmer la création ou signaler un problème (ex : utilisateur déjà existant).


### Variables d’environnement

Assure-toi qu’elles sont bien définies dans le même terminal où tu exécutes le script :

set MONGO_MIGRATION_USER=migration_user
set MONGO_MIGRATION_PASS=MigrationPass!
set MONGO_HOST=localhost
set MONGO_PORT=27017
set MONGO_DB=MedicalMigration
set MONGO_COLL=patients


Puis exécute ton script dans ce terminal :

python mongo_migration.py

➤ Étape 3 — Tester
python MedicalMigration/auth/auth_mongo.py


Puis dans mongosh :

mongosh
use admin
db.system.users.find().pretty()


pour se connecter avec les différents users :


### Admin (admin_user)

Accès complet pour gérer les utilisateurs et les bases :

mongosh -u admin_user -p SuperSecret123 --authenticationDatabase admin


-u : nom de l’utilisateur

-p : mot de passe

--authenticationDatabase : base utilisée pour authentification (ici admin)

Une fois connecté, tu peux gérer les utilisateurs, créer des bases, etc.

### Migration (migration_user)

Accès en lecture/écriture sur la base MedicalMigration uniquement :

mongosh -u migration_user -p MigrationPass! --authenticationDatabase MedicalMigration


Peut insérer, mettre à jour et supprimer des documents dans MedicalMigration.

Ne peut pas créer d’utilisateurs ni gérer d’autres bases.

### Lecture seule (read_user)

Accès limité en lecture seule sur la base MedicalMigration :

mongosh -u read_user -p ReadOnly123 --authenticationDatabase MedicalMigration


Peut seulement lire les documents (find()) dans la base MedicalMigration.

Toute tentative d’insertion, mise à jour ou suppression sera refusée.

### migration de données 
Copie-colle ce code en adaptant le chemin CSV et le nom de la base/collection si nécessaire :
```
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

```

### Exécuter le script

Assure-toi que l’environnement virtuel est activé ((venv) dans PowerShell).
```
python .\MedicalMigration\scripts\migrate_to_mongo.py
```

### Résultat attendu :

(venv) PS C:\Users\yeodr\Migration_donnees_medicales> python .\MedicalMigration\scripts\migrate_to_mongo.py 2025-10-16 22:04:43,328 - INFO - Lecture du CSV : C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv 2025-10-16 22:04:43,612 - INFO - === Diagnostic CSV === 2025-10-16 22:04:43,612 - INFO - Colonnes détectées : ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider', 'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date', 'Medication', 'Test Results'] 2025-10-16 22:04:43,613 - INFO - Nombre de lignes : 55500 2025-10-16 22:04:43,621 - INFO - Aperçu du contenu (5 premières lignes) : Name Age Gender Blood Type Medical Condition Date of Admission Doctor Hospital Insurance Provider Billing Amount Room Number Admission Type Discharge Date Medication Test Results 0 Bobby JacksOn 30 Male B- Cancer 2024-01-31 Matthew Smith Sons and Miller Blue Cross 18856.281306 328 Urgent 2024-02-02 Paracetamol Normal 1 LesLie TErRy 62 Male A+ Obesity 2019-08-20 Samantha Davies Kim Inc Medicare 33643.327287 265 Emergency 2019-08-26 Ibuprofen Inconclusive 2 DaNnY sMitH 76 Female A- Obesity 2022-09-22 Tiffany Mitchell Cook PLC Aetna 27955.096079 205 Emergency 2022-10-07 Aspirin Normal 3 andrEw waTtS 28 Female O+ Diabetes 2020-11-18 Kevin Wells Hernandez Rogers and Vang, Medicare 37909.782410 450 Elective 2020-12-18 Ibuprofen Abnormal 4 adrIENNE bEll 43 Female AB+ Cancer 2022-09-19 Kathleen Hanna White-White Aetna 14238.317814 458 Urgent 2022-10-09 Penicillin Abnormal

2025-10-16 22:04:43,649 - INFO - Connexion à MongoDB réussie : medical_db.patients!

### Optionnel 1 : Déplacer le CSV dans le dossier dataset (optionnel)
Crée le dossier dataset si ce n’est pas déjà fait :

```
mkdir C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset
```

### Déplace le CSV dedans :
```
move "C:\Users\yeodr\Migration_donnees_medicales\healthcare_dataset.csv" "C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset"
```

Vérifie :
```

dir C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset

```

Ton script migrate_to_mongo.py peut rester tel quel :
```

CSV_PATH = os.environ.get( "CSV_PATH", r"C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv" )
```



# Identification de l'adresse ip du docker (medical_mongo)
## Pour identifier l'adresse ip:
```
cd C:\Users\yeodr\Migration_donnees_medicales
```
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" medical_mongo

Depuis l’intérieur du conteneur

Tu peux aussi entrer dans le conteneur et vérifier l’IP :
```
docker exec -it medical_mongo bash
```
Puis dans le conteneur :
```
ip addr show
```
Cherche l’interface eth0.

L’IP affichée est celle du conteneur.


## l'adresse ip est ajouté au script pour favoriser la mgration, mais j'ai plutôt utilisé le nom du conteneur 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# pour voir les logs (commande : docker logs migration_script) :PS C:\Users\yeodr\Migration_donnees_medicales\docker> docker logs migration_script
Traceback (most recent call last): File "/app/scripts/migrate_to_mongo.py", line 1, in import pandas as pd File "/usr/local/lib/python3.11/site-packages/pandas/init.py", line 46, in from pandas.core.api import ( File "/usr/local/lib/python3.11/site-packages/pandas/core/api.py", line 1, in from pandas._libs import ( File "/usr/local/lib/python3.11/site-packages/pandas/_libs/init.py", line 18, in from pandas._libs.interval import Interval File "interval.pyx", line 1, in init pandas._libs.interval ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject PS C:\Users\yeodr\Migration_donnees_medicales\docker>

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Etape 6 : conteneurisez l'application avec docker


## Arborescence des fichiers
```
Migration_donnees_medicales/
│
├─ MedicalMigration/
│  ├─ scripts/
│  │  ├─ migrate_to_mongo.py        # script principal de migration (CRUD complet)
│  │  ├─ data_cleaning.py           # pré-traitement du dataset
│  │  ├─ mongo_migration.py         # fonctions MongoDB supplémentaires (si nécessaire)
│  │  └─ __pycache__/               # fichiers compilés Python
│  │
│  ├─ auth/
│  │  └─ auth_mongo.py              # gestion des utilisateurs MongoDB
│  │
│  ├─ dataset/
│  │  └─ healthcare_dataset.csv     # dataset médical source
│  │
│  ├─ __init__.py                   # rendre MedicalMigration un package Python
│  ├─ requirements.txt              # dépendances Python
│  └─ .github/
│     └─ workflows/
│        └─ ci_cd.yml               # pipeline CI/CD GitHub Actions
│
├─ docker/
│  ├─ Dockerfile                     # image Python + MongoDB client
│  └─ docker-compose.yml             # orchestration MongoDB + app
│
├─ schema/
│  └─ medical_db.patients.json       # schéma JSON de la base MongoDB
│
├─ tests/
│  ├─ test_migration.py              # tests unitaires pour migrate_to_mongo.py
│  └─ __pycache__/                   # fichiers compilés Python
│
├─ .env                              # variables d’environnement (MongoDB URI, credentials)
├─ README.md                          # documentation principale du projet
└─ .gitignore                         # fichiers à ne pas pousser (logs, CSV, venv, etc.)



```


MedicalMigration/ : contient ton code Python, le CSV et le Dockerfile.

docker/ : contient docker-compose.yml.

## Dockerfile (dans MedicalMigration/) : créer un fichier(Dockerfile) et copié

```
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/migrate_to_mongo.py"]

```

Permet de construire l’image Python qui exécutera le script de migration.



## créer un fichier requirements.txt et coller :

```
pandas==2.0.3
numpy==1.26.0
pymongo==4.6.1
python-dotenv==1.0.1

```

### le fichier requirements.txt sert à décrire tous les modules Python nécessaires pour faire fonctionner ton projet 
— c’est une liste des dépendances de ton environnement. pour le lancer :
```
pip install -r requirements.txt
```
## reconstruire l'image:
```
docker-compose up --build
```
## pour voir l’état final des conteneur
```
docker ps -a
```

## docker-compose.yml (dans docker/) : créer le fichier

```
services:
  mongo:
    image: mongo:latest
    container_name: mongo_medical
    ports:
      - "27018:27017"  # accès MongoDB depuis l'hôte
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ADMIN_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ADMIN_PASS}
      MONGO_INITDB_DATABASE: ${MONGO_DB}

      # Utilisateurs supplémentaires pour init-mongo.js
      MONGO_MIGRATION_USER: ${MONGO_MIGRATION_USER}
      MONGO_MIGRATION_PASS: ${MONGO_MIGRATION_PASS}
      MONGO_READ_USER: ${MONGO_READ_USER}
      MONGO_READ_PASS: ${MONGO_READ_PASS}
    volumes:
      - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
      - mongo_data:/data/db
    networks:
      - medical_net
    healthcheck:
      test: ["CMD-SHELL", "mongosh --eval 'db.runCommand({ ping: 1 })' || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  migration:
    build:
      context: ..                    # dossier parent
      dockerfile: docker/Dockerfile
    env_file:
      - .env                         # récupération des variables depuis le fichier .env
    depends_on:
      mongo:
        condition: service_healthy
    volumes:
      - ../MedicalMigration/dataset:/app/dataset
      - ../MedicalMigration/scripts:/app/scripts
    environment:
      MONGO_DOCKER_HOST: mongo_medical
      MONGO_DOCKER_PORT: 27017
      CSV_PATH: /app/dataset/healthcare_dataset.csv
    networks:
      - medical_net
    command: python /app/scripts/mongo_migration.py

volumes:
  mongo_data:

networks:
  medical_net:
    driver: bridge


```

Le conteneur Python utilise MONGO_HOST=mongo pour se connecter au conteneur Mongo.

## Script Python (migrate_to_mongo.py)

Assure-toi que dans le script, tu as :

```
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

```

## Comme ça, le même script fonctionne à la fois dans le conteneur docker et en local 



## Lancer le tout

Depuis le dossier docker/ :
```
docker-compose up --build
```

## Docker Compose va :

**Démarrer MongoDB avec persistance (mongo_medical)**

**Construire l’image Python**

**Exécuter automatiquement le script de migration**



## Vérification

### aller dans dockerr desktop:
ouvrir le terminal et saisir ces commandes
```
use medical_db
db.patients.countDocuments()
db.patients.findOne()
```
ou

Ouvre un shell MongoDB :
```
docker exec -it medical_mongo mongo
```

### Teste la base et la collection :
```
use medical_db
db.patients.countDocuments()
db.patients.findOne()
```

Tu devrais voir le nombre de documents insérés depuis le CSV.


# Résumé des actions réalisées

Mise en place du projet de migration des données médicales sous la supervision de Boris, dans le cadre d’un stage Data Engineer chez DataSoluTech.
Objectif : migrer un dataset médical volumineux vers MongoDB, conteneuriser la solution avec Docker, et préparer un futur déploiement sur AWS.

## Analyse et traitement du dataset healthcare_dataset.csv :

**Lecture et exploration avec Pandas.**

**Vérification du nombre de lignes (55 500) et colonnes (15).**

**Contrôle des doublons et des valeurs manquantes.**

Création de l’arborescence du projet :

```
Migration_donnees_medicales/
│
├─ MedicalMigration/
│  ├─ scripts/
│  │  ├─ migrate_to_mongo.py        # script principal de migration (CRUD complet)
│  │  ├─ data_cleaning.py           # pré-traitement du dataset
│  │  ├─ mongo_migration.py         # fonctions MongoDB supplémentaires (si nécessaire)
│  │  └─ __pycache__/               # fichiers compilés Python
│  │
│  ├─ auth/
│  │  └─ auth_mongo.py              # gestion des utilisateurs MongoDB
│  │
│  ├─ dataset/
│  │  └─ healthcare_dataset.csv     # dataset médical source
│  │
│  ├─ __init__.py                   # rendre MedicalMigration un package Python
│  ├─ requirements.txt              # dépendances Python
│  └─ .github/
│     └─ workflows/
│        └─ ci_cd.yml               # pipeline CI/CD GitHub Actions
│
├─ docker/
│  ├─ Dockerfile                     # image Python + MongoDB client
│  └─ docker-compose.yml             # orchestration MongoDB + app
│
├─ schema/
│  └─ medical_db.patients.json       # schéma JSON de la base MongoDB
│
├─ tests/
│  ├─ test_migration.py              # tests unitaires pour migrate_to_mongo.py
│  └─ __pycache__/                   # fichiers compilés Python
│
├─ .env                              # variables d’environnement (MongoDB URI, credentials)
├─ README.md                          # documentation principale du projet
└─ .gitignore                         # fichiers à ne pas pousser (logs, CSV, venv, etc.)



```

## Mise en place et test de MongoDB avec Docker Compose :

**Création du fichier docker-compose.yml.**

**Lancement du conteneur MongoDB (medical_mongo) avec persistance des données.**

**Vérification du bon fonctionnement via docker ps et mongosh.**

## Développement du script Python de migration (migrate_to_mongo.py) :

**Lecture du CSV avec Pandas.**

**Connexion à MongoDB avec PyMongo.**

**Conversion des dates et insertion des 55 500 enregistrements dans la collection patients.**

**Ajout d’index sur Name et Date of Admission.**

## Création du fichier requirements.txt :
```
pandas==2.0.3
numpy==1.26.0
pymongo==4.6.1
python-dotenv==1.0.1

```

# Liste des dépendances nécessaires à l’exécution du projet.

## Création du Dockerfile pour le conteneur Python :

**Installation des dépendances.**

**Exécution automatique du script de migration à la construction du conteneur.**

## Exécution et validation de la migration complète :

**Commande : docker-compose up --build**

**Résultat : 55 500 documents insérés dans medical_db.patients.**

## Vérification :
```
docker exec -it medical_mongo mongosh
use medical_db
db.patients.countDocuments()
```

## Gestion des erreurs rencontrées et corrections :

**Problème d’incompatibilité entre Pandas et NumPy corrigé avec les versions exactes.**

**Adaptation du script pour fonctionner à la fois en local et dans Docker grâce aux variables d’environnement.**

# Résultat final :

**Solution fonctionnelle, portable et reproductible.**

**Base MongoDB peuplée à partir du CSV.**

**Conteneurisation complète prête pour un déploiement futur sur AWS.**


# Gestion et modification des branches 

### Création des autres branches, script et test

PROCÉDURE COMPLÈTE — MIGRATION MÉDICALE (branche par branche)

Ces étapes s’appliquent à chaque branche :

feature/tests-unitaires

feature/authentification

feature/analyse-donnees

feature/configuration-docker

## SE POSITIONNER SUR LA BRANCHE PRINCIPALE

Toujours partir de la dernière version stable du projet :

cd C:\Users\yeodr\Migration_donnees_medicales
git checkout main
git pull origin main


Cela garantit que tu travailles sur la version la plus récente avant de créer une nouvelle branche.

## CRÉER LA NOUVELLE BRANCHE

Exemple :

git checkout -b feature/tests-unitaires


Répéter ensuite pour chaque fonctionnalité :

git checkout -b feature/authentification
git checkout -b feature/analyse-donnees
git checkout -b feature/configuration-docker

## CONNEXION AU NŒUD & AJOUT DU CONTENU SPÉCIFIQUE
## A. Branche : feature/tests-unitaires
➤ Étape 1 — Se placer dans le bon dossier
cd C:\Users\yeodr\Migration_donnees_medicales
mkdir tests
cd tests

➤ Étape 2 — Créer le fichier de test
notepad test_migration.py


Colle le script suivant 

```
import unittest
import pandas as pd
import sys
import os

# --- Ajouter le dossier racine pour que Python trouve le package ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from MedicalMigration.scripts.mongo_migration import (
    connect_to_mongo,
    create_documents,
    update_documents,
    delete_documents,
    read_documents
)

class TestMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Initialisation avant tous les tests"""
        # Connexion à la collection
        cls.collection = connect_to_mongo("localhost", 27017)  # adapter host/port si nécessaire
        cls.df = pd.DataFrame([
            {"Name": "TestUser_Temp", "Date of Admission": "2024-01-01", "Discharge Date": "2024-01-10"}
        ])
        # Nombre initial de documents
        cls.initial_count = cls.collection.count_documents({})

    def test_insert_data(self):
        """Test de l'insertion de documents factices"""
        create_documents(self.collection, self.df.to_dict("records"))
        docs = read_documents(self.collection, {"Name": "TestUser_Temp"})
        self.assertEqual(len(docs), 1, "L'insertion du document factice a échoué")

    def test_update_sample(self):
        """Test de la mise à jour d'un document factice"""
        update_documents(self.collection, {"Name": "TestUser_Temp"}, {"Status": "Updated"})
        updated_doc = read_documents(self.collection, {"Name": "TestUser_Temp"})[0]
        self.assertEqual(updated_doc.get("Status"), "Updated", "Le statut du document factice n'a pas été mis à jour")

    def test_delete_sample(self):
        """Test de la suppression d'un document factice"""
        delete_documents(self.collection, {"Name": "TestUser_Temp"})
        docs = read_documents(self.collection, {"Name": "TestUser_Temp"})
        self.assertEqual(len(docs), 0, "Le document factice n'a pas été supprimé")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage des documents factices"""
        delete_documents(cls.collection, {"Name": "TestUser_Temp"})
        # Vérifier que le nombre total de documents reste inchangé
        final_count = cls.collection.count_documents({})
        assert final_count == cls.initial_count, "Le nombre total de documents a changé après les tests !"

if __name__ == "__main__":
    unittest.main()
```


➤ Étape 3 — Enregistrer, puis tester
se placer :
cd C:\Users\yeodr\Migration_donnees_medicales

python -m unittest discover tests


## Résultat attendu :

..
----------------------------------------------------------------------
Ran 2 tests in X.XXXs
OK

➤ Étape 4 — Commit & Push
git add .
git commit -m "Ajout des tests unitaires du script de migration"
git push origin feature/tests-unitaires

## Branche : feature/authentification
➤ Étape 1 — Retour à main et création
git checkout main
git pull origin main
git checkout -b feature/authentification

➤ Étape 2 — Créer le répertoire et le fichier
mkdir MedicalMigration\auth
notepad MedicalMigration\auth\auth_mongo.py


Colle le script 

```
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
```


>>Se connecte au serveur MongoDB local.

Crée trois utilisateurs avec des rôles différents :

admin_user → administrateur capable de gérer toutes les bases et utilisateurs.

migration_user → peut lire et écrire dans la base MedicalMigration.

read_user → peut seulement lire les données dans la base MedicalMigration.

Utilise les mots de passe définis dans les variables d’environnement.

Affiche des logs pour confirmer la création ou signaler un problème (ex : utilisateur déjà existant).


## Variables d’environnement

Assure-toi qu’elles sont bien définies dans le même terminal où tu exécutes le script :

set MONGO_MIGRATION_USER=migration_user
set MONGO_MIGRATION_PASS=MigrationPass!
set MONGO_HOST=localhost
set MONGO_PORT=27017
set MONGO_DB=MedicalMigration
set MONGO_COLL=patients


Puis exécute ton script dans ce terminal :

python mongo_migration.py

➤ Étape 3 — Tester
python MedicalMigration/auth/auth_mongo.py


Puis dans mongosh :

mongosh
use admin
db.system.users.find().pretty()


pour se connecter avec les différents users :


## Admin (admin_user)

Accès complet pour gérer les utilisateurs et les bases :

mongosh -u admin_user -p SuperSecret123 --authenticationDatabase admin


-u : nom de l’utilisateur

-p : mot de passe

--authenticationDatabase : base utilisée pour authentification (ici admin)

Une fois connecté, tu peux gérer les utilisateurs, créer des bases, etc.

## Migration (migration_user)

Accès en lecture/écriture sur la base MedicalMigration uniquement :

mongosh -u migration_user -p MigrationPass! --authenticationDatabase MedicalMigration


Peut insérer, mettre à jour et supprimer des documents dans MedicalMigration.

Ne peut pas créer d’utilisateurs ni gérer d’autres bases.

## Lecture seule (read_user)

Accès limité en lecture seule sur la base MedicalMigration :

mongosh -u read_user -p ReadOnly123 --authenticationDatabase MedicalMigration


Peut seulement lire les documents (find()) dans la base MedicalMigration.

Toute tentative d’insertion, mise à jour ou suppression sera refusée.



## Résultat attendu :
L’utilisateur admin_user est affiché.

➤ Étape 4 — Commit & Push
git add .
git commit -m "Ajout de la gestion des utilisateurs MongoDB"
git push origin feature/authentification

## Branche : feature/analyse-donnees
➤ Étape 1 — Créer la branche
git checkout main
git pull origin main
git checkout -b feature/analyse-donnees

➤ Étape 2 — Créer le script d’analyse
mkdir MedicalMigration\scripts
notepad MedicalMigration\scripts\data_cleaning.py


Colle le script 


```
import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO)

def analyze_dataset(file_path):
    # Lecture du CSV
    df = pd.read_csv(file_path)
    
    # Nombre de lignes et colonnes
    total_rows = len(df)
    total_columns = len(df.columns)
    column_names = list(df.columns)
    
    # Nombre de doublons
    duplicate_rows = df.duplicated().sum()
    
    logging.info(f"Nombre total de lignes : {total_rows}")
    logging.info(f"Nombre total de colonnes : {total_columns}")
    logging.info(f"Colonnes : {column_names}")
    logging.info(f"Nombre de doublons : {duplicate_rows}")
    
    # Optionnel : aperçu des doublons
    if duplicate_rows > 0:
        logging.info(f"Exemple de doublons :\n{df[df.duplicated()].head()}")

if __name__ == "__main__":
    # Chemin absolu du CSV, indépendant du dossier courant
    base_dir = os.path.dirname(__file__)  # répertoire du script
    csv_path = os.path.abspath(os.path.join(base_dir, "..", "dataset", "healthcare_dataset.csv"))

    analyze_dataset(csv_path)

```



➤ Étape 3 — Tester
python MedicalMigration/scripts/data_cleaning.py


# Résultat attendu :

INFO - Lignes avant nettoyage : 55500
INFO - Lignes après nettoyage : 55492
## Données nettoyées enregistrées dans healthcare_dataset_cleaned.csv

➤ Étape 4 — Commit & Push
git add .
git commit -m "Ajout du script de nettoyage et analyse des données"
git push origin feature/analyse-donnees

## Branche : feature/configuration-docker
➤ Étape 1 — Créer la branche
git checkout main
git pull origin main
git checkout -b feature/configuration-docker

➤ Étape 2 — Créer la structure Docker
mkdir docker
cd docker
notepad Dockerfile


## Contenu du Dockerfile :

```
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


Ensuite :

notepad docker-compose.yml

```

## Contenu du docker-compose.yml :


```
services:
  mongo:
    image: mongo:latest
    container_name: mongo_medical
    ports:
      - "27018:27017"  # accès MongoDB depuis l'hôte
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ADMIN_USER}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ADMIN_PASS}
      MONGO_INITDB_DATABASE: ${MONGO_DB}

      # Utilisateurs supplémentaires pour init-mongo.js
      MONGO_MIGRATION_USER: ${MONGO_MIGRATION_USER}
      MONGO_MIGRATION_PASS: ${MONGO_MIGRATION_PASS}
      MONGO_READ_USER: ${MONGO_READ_USER}
      MONGO_READ_PASS: ${MONGO_READ_PASS}
    volumes:
      - ./init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js:ro
      - mongo_data:/data/db
    networks:
      - medical_net
    healthcheck:
      test: ["CMD-SHELL", "mongosh --eval 'db.runCommand({ ping: 1 })' || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  migration:
    build:
      context: ..                    # dossier parent
      dockerfile: docker/Dockerfile
    env_file:
      - .env                         # récupération des variables depuis le fichier .env
    depends_on:
      mongo:
        condition: service_healthy
    volumes:
      - ../MedicalMigration/dataset:/app/dataset
      - ../MedicalMigration/scripts:/app/scripts
    environment:
      MONGO_DOCKER_HOST: mongo_medical
      MONGO_DOCKER_PORT: 27017
      CSV_PATH: /app/dataset/healthcare_dataset.csv
    networks:
      - medical_net
    command: python /app/scripts/mongo_migration.py

volumes:
  mongo_data:

networks:
  medical_net:
    driver: bridge

```


➤ Étape 3 — Tester Docker
cd docker
docker-compose up --build

ou : docker build -t mongo_migration_image .




## Résultat attendu :

Le conteneur medical_mongo démarre

Le conteneur migration_script affiche
Migration terminée avec succès !

➤ Étape 4 — Commit & Push
git add .
git commit -m "Ajout de la configuration Docker pour MongoDB et le script de migration"
git push origin feature/configuration-docker

## FUSIONNER LES BRANCHES DANS MAIN (APRÈS TESTS VALIDÉS)
git checkout main
git pull origin main
git merge feature/tests-unitaires
git merge feature/authentification
git merge feature/analyse-donnees
git merge feature/configuration-docker
git push origin main


>>pour supprimer le dossier et fichier

## Avec PowerShell
Remove-Item -Recurse -Force .\tests


-Recurse : supprime tout le contenu du dossier (sous-dossiers et fichiers).

-Force : supprime même les fichiers en lecture seule.

## Avec l’invite de commandes (cmd)
rmdir /s /q tests


/s : supprime tous les fichiers et sous-dossiers.

/q : mode silencieux (pas de confirmation).

Après suppression, tu peux vérifier :

ls


ou

dir


Le dossier tests ne doit plus apparaître.

mongosh -u migration_user -p MigrationPass! --authenticationDatabase MedicalMigration
mongosh -u read_user -p readonly123 --authenticationDatabase MedicalMigration

mongosh -u admin_user -p 'securePass123' --authenticationDatabase admin


## Préparer les variables d’environnement

Tu as déjà ton fichier .env :

MONGO_ADMIN_USER=admin_user
MONGO_ADMIN_PASS=securePass123
MONGO_MIGRATION_USER=migration_user
MONGO_MIGRATION_PASS=migrationPass!
MONGO_READ_USER=read_user
MONGO_READ_PASS=readonly123


Tu dois t’assurer qu’il est chargé dans ton environnement avant d’ouvrir MongoDB Compass.
Sous Windows, tu peux faire dans le terminal (PowerShell) :

setx MONGO_ADMIN_USER "admin_user"
setx MONGO_ADMIN_PASS "securePass123"
setx MONGO_MIGRATION_USER "migration_user"
setx MONGO_MIGRATION_PASS "migrationPass!"
setx MONGO_READ_USER "read_user"
setx MONGO_READ_PASS "readonly123"


Cela définit les variables pour ton utilisateur. Tu devras redémarrer MongoDB Compass pour qu’il les reconnaisse.

## Configurer la connexion dans MongoDB Compass

Ouvre MongoDB Compass → New Connection.

Dans Hostname, mets : localhost

Dans Port, mets : 27017

Sous Authentication, choisis Username / Password.

Dans Username, mets : migration_user (ou autre user selon le rôle voulu)

Dans Password, mets : %MONGO_MIGRATION_PASS% si Compass supporte les variables d’environnement, sinon copie le mot de passe directement (c’est le point faible de Compass, il ne lit pas toujours les .env).

Dans Authentication Database, mets : MedicalMigration (ou admin pour admin_user).

Si Compass ne supporte pas les variables d’environnement dans les champs, tu devras saisir le mot de passe directement. L’avantage reste que dans les scripts Python, tu n’as plus de mots de passe en dur, seulement dans le .env.


## Depuis Docker Desktop (interface graphique)

Tu peux ouvrir un terminal MongoDB directement depuis Docker Desktop :

Ouvre Docker Desktop

Va dans l’onglet Containers

Clique sur ton conteneur mongo_medical

Clique sur "Open in terminal" ou "Exec" (selon la version)

## Cela ouvre un shell à l’intérieur du conteneur (équivalent à docker exec -it mongo_medical bash)

Une fois dans le terminal, tape :

mongosh -u migration_user -p 'migrationPass!' --authenticationDatabase medical_db


## réalisation de test 

## Test unitaire 

## test_collection_non_vide
•	But : Vérifier que la collection patients n’est pas vide après la migration.
•	Comment :
count = self.collection.count_documents({})
self.assertGreater(count, 0)
•	Ce que ça teste : Il y a au moins un document dans la collection.

## test_champs_principaux_present
•	But : Vérifier que tous les champs principaux attendus sont présents dans un document.
•	Comment :
expected_fields = ["Name", "Age", "Gender", ... , "Test Results"]
doc = self.collection.find_one()
for field in expected_fields:
    self.assertIn(field, doc)
•	Ce que ça teste : Chaque document contient bien les champs critiques comme Name, Age, Gender, Blood Type, etc.

## test_types_champs
•	But : Vérifier le type de certaines colonnes importantes.
•	Comment :
self.assertIsInstance(doc["Age"], int)
self.assertIsInstance(doc["Billing Amount"], (int, float))
self.assertIsInstance(doc["Name"], str)
self.assertIsInstance(doc["Date of Admission"], str)
•	Ce que ça teste : Les types de données sont corrects (Age entier, Billing Amount numérique, Name et Date of Admission chaînes de caractères).

## test_indexes_existants
•	But : Vérifier que des index importants existent pour optimiser les requêtes.
•	Comment :
indexes = self.collection.index_information()
self.assertIn("Name_1", indexes)
self.assertIn("Date of Admission_1", indexes)
•	Ce que ça teste : Les index sur les champs Name et Date of Admission ont bien été créés.

## test_echantillon_donnees
•	But : Vérifier certaines valeurs plausibles sur un échantillon de documents.
•	Comment :
doc = self.collection.find_one({"Age": {"$gte": 0}})
self.assertIsNotNone(doc)
self.assertIn(doc["Gender"], ["Male", "Female"])
•	Ce que ça teste :
o	Il y a au moins un patient avec un âge ≥ 0.
o	La valeur du genre est correcte (Male ou Female).

## Résumé global :
Ces tests couvrent les points essentiels d’une migration vers MongoDB :
1.	La collection n’est pas vide.
2.	Tous les champs attendus sont présents.
3.	Les types des champs sont corrects.
4.	Les index essentiels existent.
5.	Les données sont plausibles sur un échantillon.


Pour l’authentification 
•	Après exécution du script :
o	Un utilisateur MongoDB admin_user est créé dans la base admin.
o	Il peut gérer les utilisateurs et les rôles dans toutes les bases.
•	Tu devras ensuite te connecter avec ce nom d’utilisateur et ce mot de passe si l’authentification est activée.


## Automatiser le processus 
## CI : Continuous Integration (Intégration continue)

Objectif : automatiser l’intégration du code des développeurs dans un dépôt partagé.

Fonctionnement :

Chaque fois qu’un développeur pousse du code (commit) dans le dépôt, une série de tests et de vérifications est exécutée automatiquement.

On détecte rapidement les bugs ou conflits.

Avantages :

Réduction des erreurs de fusion.

Détection rapide des problèmes.

Code toujours dans un état fonctionnel.

Exemple d’outils : GitHub Actions, GitLab CI, Jenkins, CircleCI.

## CD : Continuous Delivery / Continuous Deployment (Livraison/Déploiement continu)

Continuous Delivery :

Le code validé par la CI peut être livré automatiquement dans un environnement de pré-production.

Le déploiement en production reste manuel, mais il est prêt à tout moment.

Continuous Deployment :

Le code validé par la CI est automatiquement déployé en production sans intervention humaine.

Exemple d’outils : Jenkins, GitHub Actions, GitLab CI/CD, AWS CodePipeline.

## En résumé :

Mettre en place un CI/CD, c’est créer un pipeline automatisé qui :

Intègre le code automatiquement (CI)

Teste, construit et déploie automatiquement (CD)

## Résultat : plus de rapidité, moins d’erreurs, production plus fiable.

## création des dossiers et du fichier : .github\workflows et le fichier : ci_cd.yml
## création de ces dossiers : C:\tools\act
## téléchargé de : act_Windows_x86_64.zip et il faut le dézibé ici : C:\tools\act
## contenu du fichier : 

```
name: CI - Tests unitaires

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Tests unitaires
    runs-on: ubuntu-latest
    container: python:3.11-slim

    steps:
      - name: Checkout du code
        uses: actions/checkout@v4

      - name: Installation des dépendances Python
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Exécution des tests unitaires
        working-directory: /github/workspace/MedicalMigration
        run: |
          python -m unittest discover -s tests -p "test_*.py" -v

```

## ce que fait ci_cd.yml : 

Étapes principales :

## Récupérer le code

uses: actions/checkout@v4


GitHub copie ton projet sur un ordinateur virtuel temporaire.

## Installer Python et les dépendances

pip install -r requirements.txt


Installe tous les modules Python dont ton projet a besoin (pandas, pymongo, etc.).

## Lancer les tests automatiques

python -m unittest discover -s tests -p "test_*.py" -v


Cherche tous les fichiers de test dans le dossier tests.

Vérifie que ton code fonctionne correctement.

Affiche quels tests passent et lesquels échouent.

Pourquoi c’est utile ?

Automatique : tu n’as pas besoin de lancer les tests manuellement.

Fiable : si un test échoue, GitHub te le dit immédiatement.

Sûr : tu sais que ton code ne va pas casser l’application avant de le déployer.



# Documentation — Passage au cloud AWS pour MongoDB
Objectif
Se familiariser avec le passage au cloud et les services AWS pour la gestion d’une base de données MongoDB.
Important : cette étape est uniquement documentaire et ne nécessite pas de déploiement réel.

1-Création d’un compte AWS
Pour utiliser AWS, il faut d’abord un compte. Voici comment procéder :
1.	Aller sur le site officiel AWS :
lien : https://aws.amazon.com/
2.	Cliquer sur “Create an AWS Account”.
3.	Saisir les informations demandées :
o	Adresse e-mail
o	Mot de passe
o	Nom du compte
4.	Fournir vos informations de facturation (carte bancaire, coordonnées).
5.	Vérifier votre identité via SMS ou appel téléphonique.
6.	Accéder à la console AWS, depuis laquelle tous les services sont gérés.
AWS propose un Free Tier pour tester certains services gratuitement pendant 12 mois :
lien : https://aws.amazon.com/free/

2-Comprendre la tarification AWS
<img width="841" height="288" alt="image" src="https://github.com/user-attachments/assets/edeecf84-803c-42c3-98a1-e4f40b52ae93" />

3-Services AWS pour MongoDB
Ressource	Mode de facturation	Lien
Instances compute (EC2, RDS)	par heure ou seconde selon le type	AWS Pricing

Stockage (S3, EBS, DocumentDB)	par Go / mois	AWS Pricing

I/O	certaines bases facturent les opérations de lecture/écriture	DocumentDB Pricing

Sauvegardes / snapshots	stockage supplémentaire	DocumentDB Backup

Transfert de données	vers Internet ou entre régions	AWS Data Transfer

a) Amazon DocumentDB (compatible MongoDB)
•	Service managé, compatible avec les pilotes MongoDB.
•	Automatiquement hautement disponible et sécurisé.
•	Sauvegardes automatiques quotidiennes vers S3, gestion de snapshots.
•	Réplication multi-AZ pour durabilité et haute disponibilité.
•	Coût basé sur instances, stockage, I/O, et sauvegardes.
Liens officiels :
•	Présentation : https://aws.amazon.com/documentdb/
•	Documentation : https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html
•	Tarification : https://aws.amazon.com/documentdb/pricing/
Remarque : Amazon RDS ne propose pas MongoDB natif. DocumentDB est la solution recommandée pour un service managé MongoDB sur AWS.

b) Déploiement de MongoDB conteneurisé sur Amazon ECS
Amazon ECS (Elastic Container Service) permet d’exécuter des conteneurs Docker dans le cloud AWS.
Étapes principales :
1.	Préparer le conteneur Docker :
o	Dockerfile avec votre script Python + dataset + dépendances (pandas, pymongo).
o	Tester localement avant déploiement.
2.	Créer un cluster ECS via la console AWS :
o	Choisir le type de lancement (EC2 ou Fargate).
o	Créer des tâches ECS (Task Definitions) : spécifier image Docker, ressources CPU/mémoire, volumes, variables d’environnement (ex : MONGO_HOST, MONGO_DB, CSV_PATH).
3.	Configurer les services ECS pour déployer la tâche dans le cluster :
o	Définir nombre de conteneurs à lancer.
o	Lier au VPC et aux sous-réseaux pour connectivité.
4.	Volumes et stockage :
o	Si MongoDB est dans un conteneur, attacher un volume EBS pour persistance des données.
5.	Logs et monitoring :
o	Configurer CloudWatch Logs pour récupérer les logs des conteneurs.
o	Définir alarmes CloudWatch pour CPU, mémoire, erreurs.
Liens officiels :
•	Guide ECS : https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html
•	Exemple MongoDB ECS : https://aws.amazon.com/blogs/database/deploy-a-containerized-application-with-amazon-ecs-and-connect-to-amazon-documentdb-securely/
•	Logs CloudWatch : https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html
Pratique : 
>Aller sur sur aws console login : https://aws.amazon.com/fr/console/
 <img width="809" height="292" alt="image" src="https://github.com/user-attachments/assets/233159f5-861a-4ded-9fb2-51b2d0146f8d" />

>Se connecter à son compte 
 <img width="821" height="299" alt="image" src="https://github.com/user-attachments/assets/b979576c-7c01-4eb3-920d-361057d35841" />


>>chercher dans la barre de recherche ecs 
 <img width="866" height="333" alt="image" src="https://github.com/user-attachments/assets/0dc48b26-cf93-4255-a9d3-a6fbd5857d36" />
<img width="945" height="399" alt="image" src="https://github.com/user-attachments/assets/c7699853-750f-4f41-a79a-16a553785e2e" />

>>cliquer sur cluster 
 <img width="945" height="415" alt="image" src="https://github.com/user-attachments/assets/321698d6-9d88-4e1d-bce4-8d1673670764" />

>>cliquer sur create cluster >>choisisser networking only>>cliquer sur next
 <img width="945" height="446" alt="image" src="https://github.com/user-attachments/assets/67acd4bd-3588-4860-bbf8-c04e1836e2c7" />

>>renseigner le nom du cluster>>cliquer sur created 
 
 <img width="945" height="441" alt="image" src="https://github.com/user-attachments/assets/3f26d2b8-8855-4224-938a-87b7dca9466e" />
<img width="945" height="359" alt="image" src="https://github.com/user-attachments/assets/f7a8e2b7-6cca-487e-9983-c0f53ebd47cf" />

>>cliquez sur view cluster 
 <img width="945" height="421" alt="image" src="https://github.com/user-attachments/assets/e7b2a5ec-7dda-4b35-8e19-dc408933e04c" />

>>aller dans task
 <img width="945" height="398" alt="image" src="https://github.com/user-attachments/assets/e3bcf0e4-4ba7-4a62-8de2-0faa19e4c65b" />

>>le cluster est ok mais n’a pas de task>> on aller voir l’image de mongodb qu’on souhaite déployer >>allez sur docker hub 
 <img width="750" height="371" alt="image" src="https://github.com/user-attachments/assets/07a3fd0b-309e-46bd-8059-4f68dab1c00b" />

>>choisir l’image officielle 
 <img width="945" height="250" alt="image" src="https://github.com/user-attachments/assets/d3f3fc4c-ecad-41b6-9e9d-b6592e074934" />
<img width="564" height="445" alt="image" src="https://github.com/user-attachments/assets/75739b3a-3b73-439a-bf47-1b430e2d2e8a" />

 
>>Dans tag 
 <img width="945" height="176" alt="image" src="https://github.com/user-attachments/assets/200c34e8-6683-49cd-abca-fbfc2ae91858" />

>>cliquer sur jammy (c’est l’image)
<img width="772" height="300" alt="image" src="https://github.com/user-attachments/assets/624c4a1b-1621-4813-b3fc-aa39b05e586b" />
 
>>on reviens dans la console aws pour créer task definition 
 <img width="766" height="563" alt="image" src="https://github.com/user-attachments/assets/d5f2ff96-e152-433d-abb0-8a5060574b84" />

>>Cliquez sur task definition 
 <img width="851" height="387" alt="image" src="https://github.com/user-attachments/assets/9e27e9fe-661a-4038-9762-6b92d284f062" />

>>sélectionner farget 
 <img width="804" height="389" alt="image" src="https://github.com/user-attachments/assets/11d4869e-47b6-4872-a70f-dadbd4a08999" />

>>renseigner que le nom, la taille et le cpu
 <img width="755" height="370" alt="image" src="https://github.com/user-attachments/assets/e5cc2adf-3d91-47ae-af63-f137f9898e4b" />
<img width="945" height="356" alt="image" src="https://github.com/user-attachments/assets/d060ef78-4418-4e36-8954-c42f13cc1c2c" />

 
>>cliquer sur add contenair >>renseigner le nom 
 <img width="805" height="393" alt="image" src="https://github.com/user-attachments/assets/09fd18ef-3fbd-4236-b016-1d518b104e7a" />

>>pour l’image aller sur docker hub, l’image qui avait été identifier puis faire copier-coller 
 <img width="945" height="164" alt="image" src="https://github.com/user-attachments/assets/e9c4bb3a-35bb-4085-9d97-5850afc28275" />

>>coller ici 
 <img width="945" height="619" alt="image" src="https://github.com/user-attachments/assets/8276d73f-012c-4c55-8ac1-3b0fb209d62b" />
<img width="945" height="448" alt="image" src="https://github.com/user-attachments/assets/a62edc8f-adbb-4290-a812-3030a5da2898" />


 
>>le reste des cage, laisser vide et cliquer sur add contenair 
 <img width="945" height="243" alt="image" src="https://github.com/user-attachments/assets/0c862f0a-9e39-4917-bab1-0e694123a499" />

>>au bas de la page>> cliquer sur create 
 <img width="945" height="464" alt="image" src="https://github.com/user-attachments/assets/da51e10c-202e-4f71-b38a-292c9d061d93" />

 <img width="945" height="395" alt="image" src="https://github.com/user-attachments/assets/a0bbf155-ffb5-4f79-a92e-c7a16aa370f9" />

>>cliquer sur view task definition 
 
<img width="945" height="452" alt="image" src="https://github.com/user-attachments/assets/75386474-87ab-43ac-9167-dc3e78287196" />
<img width="945" height="465" alt="image" src="https://github.com/user-attachments/assets/4a6655f3-188b-461f-801f-980df1d3f264" />


>>choisez farget 
 <img width="945" height="307" alt="image" src="https://github.com/user-attachments/assets/01ddf238-7b74-4f6e-88b3-9750caae974c" />

>>choisissez linux 
 <img width="945" height="391" alt="image" src="https://github.com/user-attachments/assets/936f2432-fbc4-440d-b545-e3fb3c07c0d6" />

>>choisissez les valeurs par défaut 
 <img width="945" height="215" alt="image" src="https://github.com/user-attachments/assets/60a5e1a7-fa0d-4e70-b3f8-b9e45363fda4" />

>>cliquez sur édite au niveau de Security group
 <img width="945" height="287" alt="image" src="https://github.com/user-attachments/assets/fdd39edc-5264-40dd-9cc0-80e0da52cf1b" />

>>cliquez sur add rule pour ajouter des roles 
 <img width="945" height="545" alt="image" src="https://github.com/user-attachments/assets/a5f42342-c0de-4174-aa42-5e7e499bbe0f" />

>>dans type choisissez custom TCP et cliquez sur sauve
 <img width="945" height="241" alt="image" src="https://github.com/user-attachments/assets/c3693620-a043-4529-9381-ec1bf7a07f4f" />

>> cliquez sur run task 
 <img width="798" height="288" alt="image" src="https://github.com/user-attachments/assets/d1c6f44f-6d00-4c86-8cac-f6db65b73a22" />

>>rafraichissez 
<img width="791" height="394" alt="image" src="https://github.com/user-attachments/assets/2542270e-20da-4f4a-b6ab-74319d903167" />
 
>>cliquez sur task (id)
 <img width="945" height="37" alt="image" src="https://github.com/user-attachments/assets/0c2899dc-4209-420b-8bf1-43cb267e6f8d" />

>>on peut voir qu’il est en runing, on peut consulter les logs 
 <img width="729" height="452" alt="image" src="https://github.com/user-attachments/assets/84430b29-3204-4b0d-8e5c-68fec28794db" />
<img width="945" height="485" alt="image" src="https://github.com/user-attachments/assets/0525e844-52c0-435a-a747-5168a4700e6d" />

 
>>on va utiliser l’adresse ip public 
>>ouvrir mongodb compas>>créer une nouvelle connection et ajouté l’adresse ip public>> cliquez sur connect 
 <img width="945" height="487" alt="image" src="https://github.com/user-attachments/assets/fe49beb2-8104-4cd7-98e4-3aa6f1aa8428" />

>>connection avec succès et mongodb fonction depuis le contenair>>vous pouvez créer une base de donnée créer des collections et ajouter les donnée
<img width="945" height="410" alt="image" src="https://github.com/user-attachments/assets/80a41f1e-3c96-4c6b-91cf-b6d53552c6d4" />

 
>>aller ensuite dans aws>>consulter les logs
 <img width="841" height="425" alt="image" src="https://github.com/user-attachments/assets/9606c181-c773-421f-ab6d-7756aae5bbdb" />
<img width="846" height="442" alt="image" src="https://github.com/user-attachments/assets/4ebe38b4-c61a-48cf-8fd3-74b9e4819b0b" />

 <img width="871" height="434" alt="image" src="https://github.com/user-attachments/assets/7a33f281-f5d8-48a7-ad3e-44d87027231b" />
<img width="945" height="453" alt="image" src="https://github.com/user-attachments/assets/6635a5ff-96ce-4547-bbba-f219ce3e6b8e" />


Lien video déploiement de mongodb dans un cluster sur aws :
https://www.youtube.com/watch?v=7QmbmHsz0x8&t=1505s


4-Sauvegardes et surveillance des bases de données
Sauvegardes
•	DocumentDB : sauvegardes automatiques sur S3, possibilité de snapshots manuels.
•	MongoDB dans ECS/EC2 :
o	mongodump / mongorestore pour backup/restore.
o	Stockage des backups sur S3.
o	Automatisation possible avec cron, Lambda, ECS scheduled tasks.
Liens utiles :
•	Backup DocumentDB : https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html
•	Backup MongoDB vers S3 : https://bansalnagesh.medium.com/backing-up-mongodb-on-aws-ec2-to-s3-b045b5727fd6
Surveillance (Monitoring)
•	Utiliser CloudWatch pour :
o	CPU, mémoire, I/O, connexions, latence.
o	Définir des alertes sur seuils critiques.
•	CloudTrail pour audit et logs API.
•	IAM pour gérer les permissions et sécuriser l’accès aux bases.
Liens utiles :
•	CloudWatch : https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html
•	CloudTrail : https://aws.amazon.com/cloudtrail/

5-Résumé et utilité pour le client
•	Scalabilité : AWS permet d’adapter facilement les ressources (compute, stockage).
•	Haute disponibilité : Multi-AZ, réplication, snapshots automatiques.
•	Maintenance réduite : services managés comme DocumentDB ou ECS pour MongoDB.
•	Sécurité : IAM, VPC, CloudTrail, CloudWatch.
•	Coût maîtrisé : tarification à l’usage et calculateur AWS.
Cette documentation constitue la base pour un futur déploiement cloud, tout en permettant au client de comprendre les bénéfices et les services adaptés à MongoDB sur AWS.

# différence entre ordinateur et server 
Un ordinateur est une machine conçue pour un usage personnel, exécutant des applications bureautiques, multimédias ou de développement. Il gère généralement un seul utilisateur à la fois et n’est pas optimisé pour fonctionner en continu.

Un serveur, en revanche, est un ordinateur spécialisé conçu pour héberger, traiter et distribuer des données ou des services à plusieurs utilisateurs ou machines simultanément via un réseau. Il dispose de matériels plus puissants, d’une haute disponibilité, d’une redondance des composants (alimentation, disques) et fonctionne 24h/24, 7j/7 pour garantir la continuité des services.


# Conclusion
## Bilan du projet et compétences acquises

Ce projet m’a permis de consolider mes compétences en ingénierie des données à travers une mise en œuvre complète :

Migration de données vers une base NoSQL (MongoDB) adaptée aux volumes massifs.

Manipulation et analyse de données avec Pandas et NumPy pour assurer la qualité des imports.

Mise en place d’un environnement conteneurisé via Docker pour garantir la portabilité et la reproductibilité du projet.

Connexion et gestion de données dans MongoDB avec PyMongo.

Sur le plan méthodologique, j’ai également acquis une meilleure compréhension du cycle de vie d’un projet Data Engineering, de la préparation du jeu de données à la préparation d’un déploiement cloud.

## Avantages de la solution conteneurisée

La conteneurisation de l’application présente plusieurs bénéfices :

Portabilité totale : le projet peut être exécuté sur n’importe quelle machine disposant de Docker, sans problème de compatibilité.

Isolation des dépendances : chaque service (MongoDB, script Python, etc.) fonctionne dans son propre environnement, évitant les conflits de versions.

Déploiement rapide et reproductible : le conteneur permet de redéployer l’environnement complet en quelques secondes.

Facilité de maintenance et de scalabilité : grâce à Docker Compose ou Kubernetes, il devient simple d’ajouter ou de mettre à jour des composants sans interrompre les services.

## Perspectives d’évolution

Plusieurs axes d’amélioration et d’évolution peuvent être envisagés pour la suite du projet :

Intégration AWS : héberger MongoDB sur Amazon DocumentDB et le conteneur sur Amazon ECS pour une meilleure scalabilité et disponibilité.

Automatisation CI/CD : mettre en place un pipeline de déploiement continu (GitHub Actions, Jenkins ou GitLab CI) pour automatiser les tests, le build et le déploiement.

Monitoring et sauvegardes automatiques : intégrer des outils comme AWS CloudWatch ou Prometheus pour la supervision et la sauvegarde automatique des bases.

Optimisation des performances : ajuster la configuration de MongoDB et de Docker pour améliorer la gestion des ressources lors de traitements massifs.

      
