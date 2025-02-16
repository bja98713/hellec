# Utilisation d'une image officielle Python (version 3.11-slim)
FROM python:3.11-slim

# Empêcher Python d'écrire des fichiers .pyc et forcer la sortie en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Définir le répertoire de travail dans le container
WORKDIR /app

# Copier le fichier requirements.txt dans le container
COPY requirements.txt /app/

# Mettre à jour pip et installer les dépendances
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copier le code source dans le container
COPY . /app/

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer l'application (en production, vous pouvez utiliser gunicorn)
CMD ["gunicorn", "CEPN.wsgi:application", "--bind", "0.0.0.0:8000"]
