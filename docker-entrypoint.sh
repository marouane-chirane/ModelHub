#!/bin/bash
set -e

# Attendre que la base de données soit prête (si PostgreSQL)
if [ -n "$DATABASE_URL" ] && [[ "$DATABASE_URL" == postgresql://* ]]; then
    echo "Attente de la base de données PostgreSQL..."
    until python -c "import psycopg2; psycopg2.connect('$DATABASE_URL')" 2>/dev/null; do
        echo "Base de données non disponible, attente..."
        sleep 2
    done
    echo "Base de données PostgreSQL prête!"
fi

# Initialiser la base de données
echo "Initialisation de la base de données..."
python init_db.py || echo "Avertissement: Erreur lors de l'initialisation de la DB (peut être déjà initialisée)"

# Lancer l'application
echo "Démarrage de l'API ModelHub..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

