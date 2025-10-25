// Sécuriser l'accès aux variables d'environnement
function requireEnv(varName) {
  const value = process.env[varName];
  if (!value) {
    throw new Error(`La variable d'environnement ${varName} n'est pas définie !`);
  }
  return value;
}

// --- Utilisateur root ---
db = db.getSiblingDB("admin");
db.createUser({
  user: requireEnv("MONGO_ADMIN_USER"),
  pwd: requireEnv("MONGO_ADMIN_PASS"),
  roles: [{ role: "root", db: "admin" }]
});

// --- Utilisateur migration ---
const dbName = requireEnv("MONGO_DB");
db = db.getSiblingDB(dbName);
db.createUser({
  user: requireEnv("MONGO_MIGRATION_USER"),
  pwd: requireEnv("MONGO_MIGRATION_PASS"),
  roles: [{ role: "readWrite", db: dbName }]
});

// --- Utilisateur lecture seule ---
db.createUser({
  user: requireEnv("MONGO_READ_USER"),
  pwd: requireEnv("MONGO_READ_PASS"),
  roles: [{ role: "read", db: dbName }]
});
