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

```

## Étape 3 : MongoDB conteneurisé
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


## Étape 4 : Script Python de migration vers MongoDB
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

## Créer le script Python de migration

### Crée le fichier migrate_to_mongo.py dans le dossier scripts :
```
notepad .\MedicalMigration\scripts\migrate_to_mongo.py
```

Copie-colle ce code en adaptant le chemin CSV et le nom de la base/collection si nécessaire :

```
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


```

### Exécuter le script

Assure-toi que l’environnement virtuel est activé ((venv) dans PowerShell).
```
python .\MedicalMigration\scripts\migrate_to_mongo.py
```

### Résultat attendu :

(venv) PS C:\Users\yeodr\Migration_donnees_medicales> python .\MedicalMigration\scripts\migrate_to_mongo.py 2025-10-16 22:04:43,328 - INFO - Lecture du CSV : C:\Users\yeodr\Migration_donnees_medicales\MedicalMigration\dataset\healthcare_dataset.csv 2025-10-16 22:04:43,612 - INFO - === Diagnostic CSV === 2025-10-16 22:04:43,612 - INFO - Colonnes détectées : ['Name', 'Age', 'Gender', 'Blood Type', 'Medical Condition', 'Date of Admission', 'Doctor', 'Hospital', 'Insurance Provider', 'Billing Amount', 'Room Number', 'Admission Type', 'Discharge Date', 'Medication', 'Test Results'] 2025-10-16 22:04:43,613 - INFO - Nombre de lignes : 55500 2025-10-16 22:04:43,621 - INFO - Aperçu du contenu (5 premières lignes) : Name Age Gender Blood Type Medical Condition Date of Admission Doctor Hospital Insurance Provider Billing Amount Room Number Admission Type Discharge Date Medication Test Results 0 Bobby JacksOn 30 Male B- Cancer 2024-01-31 Matthew Smith Sons and Miller Blue Cross 18856.281306 328 Urgent 2024-02-02 Paracetamol Normal 1 LesLie TErRy 62 Male A+ Obesity 2019-08-20 Samantha Davies Kim Inc Medicare 33643.327287 265 Emergency 2019-08-26 Ibuprofen Inconclusive 2 DaNnY sMitH 76 Female A- Obesity 2022-09-22 Tiffany Mitchell Cook PLC Aetna 27955.096079 205 Emergency 2022-10-07 Aspirin Normal 3 andrEw waTtS 28 Female O+ Diabetes 2020-11-18 Kevin Wells Hernandez Rogers and Vang, Medicare 37909.782410 450 Elective 2020-12-18 Ibuprofen Abnormal 4 adrIENNE bEll 43 Female AB+ Cancer 2022-09-19 Kathleen Hanna White-White Aetna 14238.317814 458 Urgent 2022-10-09 Penicillin Abnormal

2025-10-16 22:04:43,649 - INFO - Connexion à MongoDB réussie : medical_db.patients!

### Option 1 : Déplacer le CSV dans le dossier dataset (optionnel)
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


## l'adresse ip est ajouté au script pour favoriser la mgration, mais j'ai plutôt utilisé le nom du contenaire 

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# pour voir les logs (commande : docker logs migration_script) :PS C:\Users\yeodr\Migration_donnees_medicales\docker> docker logs migration_script
Traceback (most recent call last): File "/app/scripts/migrate_to_mongo.py", line 1, in import pandas as pd File "/usr/local/lib/python3.11/site-packages/pandas/init.py", line 46, in from pandas.core.api import ( File "/usr/local/lib/python3.11/site-packages/pandas/core/api.py", line 1, in from pandas._libs import ( File "/usr/local/lib/python3.11/site-packages/pandas/_libs/init.py", line 18, in from pandas._libs.interval import Interval File "interval.pyx", line 1, in init pandas._libs.interval ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject PS C:\Users\yeodr\Migration_donnees_medicales\docker>

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Etape 4 : conteneurisez l'application avec docker


## Arborescence des fichiers
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
pandas==2.1.0
numpy==1.26.0
pymongo==4.6.1
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
version: '3.8'

services:
  mongo:
    image: mongo:latest
    container_name: medical_mongo
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db          # Volume pour persistance MongoDB
    restart: always

  python_migration:
    build:
      context: ../MedicalMigration     # Chemin vers ton Dockerfile et scripts
    container_name: migration_script
    depends_on:
      - mongo
    volumes:
      - ../MedicalMigration/dataset:/app/dataset   # Volume pour le CSV
    environment:
      - MONGO_HOST=mongo             # Nom du service Mongo pour Docker
      - MONGO_PORT=27017
      - MONGO_DB=medical_db
      - MONGO_COLL=patients
      - CSV_PATH=/app/dataset/healthcare_dataset.csv
    command: ["python", "scripts/migrate_to_mongo.py"]

volumes:
  mongo_data: {}

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


```

## Comme ça, le même script fonctionne dans Docker et peut être adapté à un MongoDB local si nécessaire.



## Lancer le tout

Depuis le dossier docker/ :
```
docker-compose up --build
```

## Docker Compose va :

**Démarrer MongoDB avec persistance (mongo_data)**

**Construire l’image Python**

**Exécuter automatiquement le script de migration**



## Vérification

### aller dans odcker desktop:
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
├─ MedicalMigration/
│  ├─ scripts/migrate_to_mongo.py
│  ├─ dataset/healthcare_dataset.csv
│  ├─ Dockerfile
│  └─ requirements.txt
└─ docker/docker-compose.yml
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
pandas==2.1.0
numpy==1.26.0
pymongo==4.6.1

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

