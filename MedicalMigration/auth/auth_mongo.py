from pymongo import MongoClient

def create_admin_user():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["admin"]

    db.command("createUser", "admin_user", pwd="securePass123", roles=[{"role": "userAdminAnyDatabase", "db": "admin"}])
    print("Utilisateur admin_user créé avec succès.")

if __name__ == "__main__":
    create_admin_user()
