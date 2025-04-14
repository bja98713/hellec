# Utilise l’image officielle Python
FROM python:3.11-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers de ton projet dans le conteneur
COPY . /app/

# Installe les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Spécifie la variable d'environnement
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose le port Django
EXPOSE 8000

# Commande à exécuter pour démarrer Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]