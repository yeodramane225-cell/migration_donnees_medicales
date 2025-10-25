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
