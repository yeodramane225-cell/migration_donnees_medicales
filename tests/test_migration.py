import unittest
from pymongo import MongoClient

class TestMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Connexion à MongoDB une seule fois pour tous les tests"""
        cls.client = MongoClient("mongodb://localhost:27017/")
        cls.db = cls.client["medical_db"]
        cls.collection = cls.db["patients"]

    def test_collection_non_vide(self):
        """La collection doit contenir des documents"""
        count = self.collection.count_documents({})
        self.assertGreater(count, 0, "La collection doit contenir des documents après migration")

    def test_champs_principaux_present(self):
        """Tous les champs attendus doivent être présents dans un document"""
        doc = self.collection.find_one()
        expected_fields = [
            "Name", "Age", "Gender", "Blood Type", "Medical Condition",
            "Date of Admission", "Doctor", "Hospital", "Insurance Provider",
            "Billing Amount", "Room Number", "Admission Type", "Discharge Date",
            "Medication", "Test Results"
        ]
        for field in expected_fields:
            self.assertIn(field, doc, f"Le champ '{field}' doit être présent dans le document")

    def test_types_champs(self):
        """Vérification du type de certaines colonnes"""
        doc = self.collection.find_one()
        self.assertIsInstance(doc["Age"], int, "Age doit être un entier")
        self.assertIsInstance(doc["Billing Amount"], (int, float), "Billing Amount doit être numérique")
        self.assertIsInstance(doc["Name"], str, "Name doit être une chaîne de caractères")
        self.assertIsInstance(doc["Date of Admission"], str, "Date of Admission doit être une chaîne de caractères")

    def test_indexes_existants(self):
        """Vérifie que les index sur Name et Date of Admission existent"""
        indexes = self.collection.index_information()
        self.assertIn("Name_1", indexes, "Index sur 'Name' manquant")
        self.assertIn("Date of Admission_1", indexes, "Index sur 'Date of Admission' manquant")

    def test_echantillon_donnees(self):
        """Vérifie certaines valeurs plausibles sur un échantillon"""
        doc = self.collection.find_one({"Age": {"$gte": 0}})
        self.assertIsNotNone(doc, "Il doit y avoir au moins un patient avec un Age >= 0")
        self.assertIn(doc["Gender"], ["Male", "Female"], "Gender doit être Male ou Female")

if __name__ == "__main__":
    unittest.main()
