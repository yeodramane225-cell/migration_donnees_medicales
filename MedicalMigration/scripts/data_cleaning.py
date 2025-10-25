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
