# Utiliser une image Python officielle comme base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer PyTorch CPU-first (beaucoup plus léger que CUDA)
# Cela évite de télécharger 2GB+ de dépendances CUDA inutiles
RUN pip install --default-timeout=300 --retries=5 \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Installer les autres dépendances (sans torch/torchvision)
# Use layer cache when requirements.txt unchanged
RUN pip install --default-timeout=300 --retries=5 -r requirements.txt

# Copier le reste du code
COPY . .

# Rendre le script de démarrage exécutable
RUN chmod +x docker-entrypoint.sh

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Utiliser le script d'entrée pour initialiser la DB et démarrer l'API
# Utiliser sh pour éviter les problèmes de permissions
ENTRYPOINT ["sh", "docker-entrypoint.sh"] 