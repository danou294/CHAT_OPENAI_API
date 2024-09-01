# Dockerfile

# Utilisez une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source de l'application
COPY . .

# Variables d'environnement
ENV DJANGO_SETTINGS_MODULE=OpenAichat.settings
ENV PYTHONUNBUFFERED=1

# Exposer le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "OpenAichat.wsgi:application"]
