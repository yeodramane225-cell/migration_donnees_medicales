# Migration des Données Médicales vers MongoDB avec Docker

![migration_des_donnees](https://github.com/user-attachments/assets/4caec7d1-9d12-41ef-a7f4-380f393cf52e)


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


## Étape 0 : Préparation

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


## Étape 1 : Structure du projet

Crée un dossier projet Migration_donnees_medicales :

## Arborescence du projet

```
Migration_donnees_medicales/
│
├─ MedicalMigration/
│  ├─ scripts/
│  │  └─ migrate_to_mongo.py
│  ├─ dataset/
│  │  └─ healthcare_dataset.csv
│  ├─ Dockerfile
│  └─ requirements.txt
│
└─ docker/
   └─ docker-compose.yml
```
## Etape 2 : analyse et traitement de healthcare_dataset.csv

```python
import pandas as pd
# Chemin du fichier CSV
file_path = "/content/healthcare_dataset.csv"

# Lire le CSV
df = pd.read_csv(file_path)

# Informations générales
print("=== Informations sur le dataset ===")
print(f"Nombre de lignes : {df.shape[0]}")
print(f"Nombre de colonnes : {df.shape[1]}")
print("\nColonnes et types :")
print(df.dtypes)

#Informations sur le dataset
#Informations sur le dataset === Nombre de lignes : 55500 Nombre de colonnes : 15

#les colonnes : Colonnes et types : Name object Age int64 Gender object Blood Type object Medical Condition object Date of Admission object Doctor object Hospital object #Insurance Provider object Billing Amount float64 Room Number int64 Admission Type object Discharge Date object Medication object Test Results object dtype: object

# Vérifier les doublons
num_doublons = df.duplicated().sum()
print(f"\nNombre de doublons : {num_doublons}")

#faux doublons détectés 

# Vérifier les valeurs manquantes
print("\n=== Valeurs manquantes par colonne ===")
print(df.isnull().sum())


--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Étape 2 : MongoDB conteneurisé
1️⃣ Créer l’arborescence du projet

Dans ton projet, crée un dossier docker :

#mkdir docker cd docker

Puis, crée le fichier docker-compose.yml :

Utiliser le Bloc-notes

--Dans PowerShell :

notepad docker-compose.yml

Si le fichier n’existe pas, il te demandera de le créer.

Colle ensuite ton contenu YAML et enregistre.

--Utiliser Visual Studio Code (si installé)

Si tu as VS Code :

code docker-compose.yml

Cela ouvrira le fichier dans VS Code.

Tu peux le modifier et sauvegarder directement.

--dans linux nano docker-compose.yml

Copie-colle le contenu suivant :

version: '3.8'

services: mongo: image: mongo:latest container_name: medical_mongo ports: - "27017:27017" volumes: - mongo_data:/data/db

volumes: mongo_data:

Enregistre et ferme le fichier.

2️⃣ Lancer MongoDB avec Docker Compose

Assure-toi que tu es dans le dossier docker où se trouve docker-compose.yml puis exécute :

docker-compose up -d

L’option -d lance le conteneur en arrière-plan (détaché).

Docker va télécharger l’image officielle mongo:latest si elle n’existe pas encore.

3️⃣ Vérifier que le conteneur tourne

Pour voir les conteneurs en cours d’exécution :

#docker ps

Tu devrais voir quelque chose comme :

CONTAINER ID IMAGE COMMAND STATUS PORTS NAMES abcd1234 mongo:latest "docker-entrypoint.s…" Up 10s 0.0.0.0:27017->27017/tcp medical_mongo

STATUS: Up → MongoDB fonctionne.

PORTS: 27017 → tu peux te connecter à MongoDB depuis ton script Python ou Mongo Shell sur ce port.

4️⃣ Tester la connexion à MongoDB (optionnel)

--on peut aller dans le shell de mongodb depuis le contenaire et fait : mongosh

on verra normalement mongodb se connecter (base test apparait)

--on peut aussi depuis vscode : aller dans le dossier (exemeple cd : C:\Users\yeodr\Migration_donnees_medicales\docker) et fait : docker exec -it medical_mongo mongosh

Si tu as installé pymongo en Python :

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") db = client.test_db print(db.list_collection_names())

Tu devrais voir une liste vide pour l’instant, car aucune collection n’est encore créée.

---------------------------------------------------------------------------------------------------------------------------------------------------------------


Étape 3 : MongoDB conteneurisé
1️⃣ Créer l’arborescence du projet

Dans ton projet, crée un dossier docker :

mkdir docker cd docker

Puis, crée le fichier docker-compose.yml :

Utiliser le Bloc-notes

--Dans PowerShell :

notepad docker-compose.yml

Si le fichier n’existe pas, il te demandera de le créer.

Colle ensuite ton contenu YAML et enregistre.

--Utiliser Visual Studio Code (si installé)

Si tu as VS Code :

code docker-compose.yml

Cela ouvrira le fichier dans VS Code.

Tu peux le modifier et sauvegarder directement.

--dans linux nano docker-compose.yml

Copie-colle le contenu suivant :

version: '3.8'

services: mongo: image: mongo:latest container_name: medical_mongo ports: - "27017:27017" volumes: - mongo_data:/data/db

volumes: mongo_data:

Enregistre et ferme le fichier.

2️⃣ Lancer MongoDB avec Docker Compose

Assure-toi que tu es dans le dossier docker où se trouve docker-compose.yml puis exécute :

docker-compose up -d

L’option -d lance le conteneur en arrière-plan (détaché).

Docker va télécharger l’image officielle mongo:latest si elle n’existe pas encore.

3️⃣ Vérifier que le conteneur tourne

Pour voir les conteneurs en cours d’exécution :

docker ps

Tu devrais voir quelque chose comme :

CONTAINER ID IMAGE COMMAND STATUS PORTS NAMES abcd1234 mongo:latest "docker-entrypoint.s…" Up 10s 0.0.0.0:27017->27017/tcp medical_mongo

STATUS: Up → MongoDB fonctionne.

PORTS: 27017 → tu peux te connecter à MongoDB depuis ton script Python ou Mongo Shell sur ce port.

4️⃣ Tester la connexion à MongoDB (optionnel)

--on peut aller dans le shell de mongodb depuis le contenaire et fait : mongosh

on verra normalement mongodb se connecter (base test apparait)

--on peut aussi depuis vscode : aller dans le dossier (exemeple cd : C:\Users\yeodr\Migration_donnees_medicales\docker) et fait : docker exec -it medical_mongo mongosh

Si tu as installé pymongo en Python :

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/") db = client.test_db print(db.list_collection_names())

Tu devrais voir une liste vide pour l’instant, car aucune collection n’est encore créée.

Étape 3 : Script Python de migration vers MongoDB
1️⃣ Créer l’environnement virtuel Python

Ouvre PowerShell et place-toi dans le dossier du projet :

cd C:\Users\yeodr\Migration_donnees_medicales

Crée un environnement virtuel appelé venv :

python -m venv venv

Active l’environnement virtuel :

.\venv\Scripts\Activate.ps1

Tu devrais voir (venv) au début de la ligne PowerShell. Cela signifie que tu es dans un environnement Python isolé.

Optionnel : mets à jour pip :

python -m pip install --upgrade pip

2️⃣ Installer les dépendances Python

Crée un dossier scripts dans ton projet si ce n’est pas déjà fait :

mkdir .\MedicalMigration\scripts

Crée le fichier requirements.txt dans ce dossier :

notepad .\MedicalMigration\scripts\requirements.txt

Copie-colle dedans :

pandas pymongo

Installe les modules dans l’environnement virtuel :

pip install -r .\MedicalMigration\scripts\requirements.txt

✅ À ce stade, ton environnement virtuel est prêt avec pandas et pymongo installés.

3️⃣ Créer le script Python de migration

Crée le fichier migrate_to_mongo.py dans le dossier scripts :

notepad .\MedicalMigration\scripts\migrate_to_mongo.py

Copie-colle ce code en adaptant le chemin CSV et le nom de la base/collection si nécessaire :

import pandas as pd from pymongo import MongoClient, errors import os import sys import logging

=== Configuration via variables d'environnement ===
Détection automatique :
- Si variable MONGO_HOST est définie (ex: Docker), utilise sa valeur
- Sinon, utilise localhost pour MongoDB local
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost") MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017)) DB_NAME = os.environ.get("MONGO_DB", "medical_db") COLLECTION_NAME = os.environ.get("MONGO_COLL", "patients")

CSV_PATH = os.environ.get( "CSV_PATH", r"C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv" )

=== Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

=== Lecture du CSV ===
try: logging.info(f"Lecture du CSV : {CSV_PATH}")

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
except Exception as e: logging.error(f"Impossible de lire le CSV : {e}") sys.exit(1)

if len(df) == 0: logging.warning("Le fichier CSV est vide. Vérifie le séparateur ou le chemin.") sys.exit(1)

=== Connexion à MongoDB ===
try: client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000) client.admin.command('ping') # Test de connexion db = client[DB_NAME] collection = db[COLLECTION_NAME] logging.info(f"Connexion à MongoDB réussie : {DB_NAME}.{COLLECTION_NAME}") except errors.ServerSelectionTimeoutError as e: logging.error(f"Impossible de se connecter à MongoDB : {e}") sys.exit(1)

=== Optionnel : vider la collection avant insertion ===
try: deleted_count = collection.delete_many({}).deleted_count if deleted_count > 0: logging.info(f"Collection vidée : {deleted_count} documents supprimés.") except Exception as e: logging.error(f"Erreur lors de la purge de la collection : {e}")

=== Insertion des données ===
try: result = collection.insert_many(df.to_dict("records")) logging.info(f"Migration terminée avec succès ! {len(result.inserted_ids)} documents insérés.")

# Création d'index
if 'Name' in df.columns:
    collection.create_index('Name')
if 'Date of Admission' in df.columns:
    collection.create_index('Date of Admission')
logging.info("Index créés sur 'Name' et 'Date of Admission'.")
except Exception as e: logging.error(f"Erreur lors de l’insertion : {e}")

Exécuter le script

Assure-toi que l’environnement virtuel est activé ((venv) dans PowerShell).

Exécute le script :

python .\MedicalMigration\scripts\migrate_to_mongo.py

✅ Résultat attendu :

(venv) PS C:\Users\yeodr\Migration_donnees_medicales> python .\MedicalMigration\scripts\migrate_to_mongo.py 2025-10-16 22:04:43,328 - INFO - Lecture du CSV : C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv 2025-10-16 22:04:43,612 - INFO - === Diagnostic CSV === 2025-10-16 22:04:43,612 - INFO - Colonnes détectées : ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider', 'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date', 'Medication', 'Test Results'] 2025-10-16 22:04:43,613 - INFO - Nombre de lignes : 55500 2025-10-16 22:04:43,621 - INFO - Aperçu du contenu (5 premières lignes) : Name Age Gender Blood Type Medical Condition Date of Admission Doctor Hospital Insurance Provider Billing Amount Room Number Admission Type Discharge Date Medication Test Results 0 Bobby JacksOn 30 Male B- Cancer 2024-01-31 Matthew Smith Sons and Miller Blue Cross 18856.281306 328 Urgent 2024-02-02 Paracetamol Normal 1 LesLie TErRy 62 Male A+ Obesity 2019-08-20 Samantha Davies Kim Inc Medicare 33643.327287 265 Emergency 2019-08-26 Ibuprofen Inconclusive 2 DaNnY sMitH 76 Female A- Obesity 2022-09-22 Tiffany Mitchell Cook PLC Aetna 27955.096079 205 Emergency 2022-10-07 Aspirin Normal 3 andrEw waTtS 28 Female O+ Diabetes 2020-11-18 Kevin Wells Hernandez Rogers and Vang, Medicare 37909.782410 450 Elective 2020-12-18 Ibuprofen Abnormal 4 adrIENNE bEll 43 Female AB+ Cancer 2022-09-19 Kathleen Hanna White-White Aetna 14238.317814 458 Urgent 2022-10-09 Penicillin Abnormal

2025-10-16 22:04:43,649 - INFO - Connexion à MongoDB réussie : medical_db.patients
!

Option 1 : Déplacer le CSV dans le dossier dataset (optionnel)
Crée le dossier dataset si ce n’est pas déjà fait :

mkdir C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset

Déplace le CSV dedans :

move "C:\Users\yeodr\Migration_donnees_medicales\healthcare_dataset.csv" "C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset"

Vérifie :

dir C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset

Ton script migrate_to_mongo.py peut rester tel quel :

CSV_PATH = os.environ.get( "CSV_PATH", r"C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv" )


--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pour identifier l'adresse ip:
cd C:\Users\yeodr\Migration_donnees_medicales

docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" medical_mongo

Depuis l’intérieur du conteneur

Tu peux aussi entrer dans le conteneur et vérifier l’IP :

docker exec -it medical_mongo bash

Puis dans le conteneur :

ip addr show

Cherche l’interface eth0.

L’IP affichée est celle du conteneur.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# pour voir les logs (commande : docker logs migration_script) :PS C:\Users\yeodr\Migration_donnees_medicales\docker> docker logs migration_script
Traceback (most recent call last): File "/app/scripts/migrate_to_mongo.py", line 1, in import pandas as pd File "/usr/local/lib/python3.11/site-packages/pandas/init.py", line 46, in from pandas.core.api import ( File "/usr/local/lib/python3.11/site-packages/pandas/core/api.py", line 1, in from pandas._libs import ( File "/usr/local/lib/python3.11/site-packages/pandas/_libs/init.py", line 18, in from pandas._libs.interval import Interval File "interval.pyx", line 1, in init pandas._libs.interval ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject PS C:\Users\yeodr\Migration_donnees_medicales\docker>

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Etape 4 : conteneurisez l'application avec docker
1️⃣ Arborescence des fichiers Migration_donnees_medicales/ │ ├─ MedicalMigration/ │ ├─ scripts/ │ │ └─ migrate_to_mongo.py │ ├─ dataset/ │ │ └─ healthcare_dataset.csv │ ├─ Dockerfile │ └─ requirements.txt │ └─ docker/ └─ docker-compose.yml

MedicalMigration/ : contient ton code Python, le CSV et le Dockerfile.

docker/ : contient docker-compose.yml.

2️⃣ Dockerfile (dans MedicalMigration/) : créer un fichier(Dockerfile) et copié

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "scripts/migrate_to_mongo.py"]

Permet de construire l’image Python qui exécutera le script de migration.

3️⃣ créer un fichier requirements.txt et coller :

pandas==2.1.0 numpy==1.26.0 pymongo==4.6.1

reconstruire l'image:

docker-compose up --build

# pour voir l’état final des conteneur

docker ps -a

4️⃣ docker-compose.yml (dans docker/) : créer le fichier

version: '3.8'

services: mongo: image: mongo:latest container_name: medical_mongo ports: - "27017:27017" volumes: - mongo_data:/data/db # Volume pour persistance MongoDB restart: always

python_migration: build: context: ../MedicalMigration # Chemin vers ton Dockerfile et scripts container_name: migration_script depends_on: - mongo volumes: - ../MedicalMigration/dataset:/app/dataset # Volume pour le CSV environment: - MONGO_HOST=mongo # Nom du service Mongo pour Docker - MONGO_PORT=27017 - MONGO_DB=medical_db - MONGO_COLL=patients - CSV_PATH=/app/dataset/healthcare_dataset.csv command: ["python", "scripts/migrate_to_mongo.py"]

volumes: mongo_data: {}

Le conteneur Python utilise MONGO_HOST=mongo pour se connecter au conteneur Mongo.

5️⃣ Script Python (migrate_to_mongo.py)

Assure-toi que dans le script, tu as :

import pandas as pd from pymongo import MongoClient, errors import os import sys import logging

=== Configuration via variables d'environnement ===
Détection automatique :
- Si variable MONGO_HOST est définie (ex: Docker), utilise sa valeur
- Sinon, utilise localhost pour MongoDB local
MONGO_HOST = os.environ.get("MONGO_HOST", "localhost") MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017)) DB_NAME = os.environ.get("MONGO_DB", "medical_db") COLLECTION_NAME = os.environ.get("MONGO_COLL", "patients")

CSV_PATH = os.environ.get( "CSV_PATH", r"C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv" )

=== Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

=== Lecture du CSV ===
try: logging.info(f"Lecture du CSV : {CSV_PATH}")

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
except Exception as e: logging.error(f"Impossible de lire le CSV : {e}") sys.exit(1)

if len(df) == 0: logging.warning("Le fichier CSV est vide. Vérifie le séparateur ou le chemin.") sys.exit(1)

=== Connexion à MongoDB ===
try: client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/", serverSelectionTimeoutMS=5000) client.admin.command('ping') # Test de connexion db = client[DB_NAME] collection = db[COLLECTION_NAME] logging.info(f"Connexion à MongoDB réussie : {DB_NAME}.{COLLECTION_NAME}") except errors.ServerSelectionTimeoutError as e: logging.error(f"Impossible de se connecter à MongoDB : {e}") sys.exit(1)

=== Optionnel : vider la collection avant insertion ===
try: deleted_count = collection.delete_many({}).deleted_count if deleted_count > 0: logging.info(f"Collection vidée : {deleted_count} documents supprimés.") except Exception as e: logging.error(f"Erreur lors de la purge de la collection : {e}")

=== Insertion des données ===
try: result = collection.insert_many(df.to_dict("records")) logging.info(f"Migration terminée avec succès ! {len(result.inserted_ids)} documents insérés.")

# Création d'index
if 'Name' in df.columns:
    collection.create_index('Name')
if 'Date of Admission' in df.columns:
    collection.create_index('Date of Admission')
logging.info("Index créés sur 'Name' et 'Date of Admission'.")
except Exception as e: logging.error(f"Erreur lors de l’insertion : {e}")

Comme ça, le même script fonctionne dans Docker et peut être adapté à un MongoDB local si nécessaire.

6️⃣ Lancer le tout

Depuis le dossier docker/ :

docker-compose up --build

Docker Compose va :

Démarrer MongoDB avec persistance (mongo_data)

Construire l’image Python

Exécuter automatiquement le script de migration

7️⃣ Vérification

aller dans odcker desktop: ouvrir le terminal et saisir ces commandes

use medical_db db.patients.countDocuments() db.patients.findOne()

ou

Ouvre un shell MongoDB :

docker exec -it medical_mongo mongo

Teste la base et la collection :

use medical_db db.patients.countDocuments() db.patients.findOne()

Tu devrais voir le nombre de documents insérés depuis le CSV.


