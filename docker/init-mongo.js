// --- Initialisation MongoDB dans Docker ---

// --- Utilisateur root ---
db = db.getSiblingDB("admin");
db.createUser({
  user: process.env.MONGO_INITDB_ROOT_USERNAME,
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [{ role: "root", db: "admin" }]
});

// --- Base pour la migration ---
const dbName = process.env.MONGO_INITDB_DATABASE;
db = db.getSiblingDB(dbName);

// --- Utilisateur migration ---
db.createUser({
  user: process.env.MONGO_MIGRATION_USER,
  pwd: process.env.MONGO_MIGRATION_PASS,
  roles: [{ role: "readWrite", db: dbName }]
});

// --- Utilisateur lecture seule ---
db.createUser({
  user: process.env.MONGO_READ_USER,
  pwd: process.env.MONGO_READ_PASS,
  roles: [{ role: "read", db: dbName }]
});
