import pandas as pd
import logging

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
    analyze_dataset("MedicalMigration/dataset/healthcare_dataset.csv")
