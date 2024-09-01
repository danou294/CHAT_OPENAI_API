# Mini Chatbot avec FastAPI et OpenAI

Ce projet implémente un mini chatbot utilisant FastAPI et l'API OpenAI. L'application permet de générer des réponses de chatbot basées sur des messages utilisateur, en utilisant le modèle GPT-3.5-turbo.

## Prérequis

- Python 3.9 ou supérieur
- Docker (facultatif, si vous souhaitez exécuter l'application dans un conteneur)

## Installation et Configuration

### 1. Cloner le dépôt

Clonez le projet depuis votre dépôt Git local :

```bash
git clone https://github.com/danou294/OPENAI-API.git
cd OPENAI-API.git
```

### 2. Configurer les variables d'environnement

Créez un fichier .env à la racine du projet et ajoutez votre clé API OpenAI :

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Créer un environnement virtuel

Il est recommandé de créer un environnement virtuel pour gérer les dépendances du projet :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
````

### 4. Installer les dépendances

Installez les dépendances du projet listées dans le fichier requirements.txt :

```bash
pip install -r requirements.txt
```

## Lancer l'application

### 1. Exécuter localement avec Uvicorn

Exécutez la commande suivante pour démarrer l'application localement :

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse http://127.0.0.1:8000.

### 2. Exécuter avec Docker

Si vous préférez utiliser Docker, suivez les étapes suivantes :

#### a. Construire et lancer l'image Docker

```bash
docker-compose up --build 
```

L'application sera accessible à l'adresse http://localhost.

## Utilisation

Une fois l'application en cours d'exécution, vous pouvez interagir avec le chatbot en envoyant des requêtes POST au point de terminaison /chat.

### Exemple de requête

Routes pour les Sessions de Chat
Créer une session de chat :

URL: `/sessions/create/`

Vue associée: `create_session`

Description: Crée une nouvelle session de chat.

Méthode HTTP: POST

Exemple de requête curl:

```bash
curl -X POST "http://localhost:8000/sessions/create/" \
-H "Content-Type: application/json" \
-d '{}'
```

Lister toutes les sessions de chat :

URL: `/sessions/`

Vue associée: `list_sessions`

Description: Récupère une liste de toutes les sessions de chat existantes.

Méthode HTTP: GET

Exemple de requête curl:

```bash
curl -X GET "http://localhost:8000/sessions/"
```

Supprimer une session de chat :

URL: `/sessions/<int:session_id>/delete/`

Vue associée: `delete_session`

Description: Supprime une session de chat spécifique en utilisant son ID.

Méthode HTTP: DELETE

Exemple de requête curl:

```bash
curl -X DELETE "http://localhost:8000/sessions/1/delete/"
```

Remplacez 1 par l'ID de la session que vous souhaitez supprimer.

Routes pour les Messages
Ajouter un message à une session de chat :

URL: `/messages/<int:session_id>/add/`

Vue associée: `add_message`

Description: Ajoute un nouveau message à une session de chat spécifique.

Méthode HTTP: POST

Exemple de requête curl:

```bash
curl -X POST "http://localhost:8000/messages/1/add/" \
-H "Content-Type: application/json" \
-d '{
    "message": "Quels sont les avantages d'utiliser Python?"
}'
```

Remplacez 1 par l'ID de la session à laquelle vous souhaitez ajouter le message.

Supprimer un message spécifique :

URL: `/messages/<int:message_id>/delete/`

Vue associée: `delete_message`

Description: Supprime un message spécifique en utilisant son ID.

Méthode HTTP: DELETE

Exemple de requête curl:

```bash
curl -X DELETE "http://localhost:8000/messages/1/delete/"
```

Remplacez 1 par l'ID du message que vous souhaitez supprimer.

Obtenir tous les messages d'une session de chat :

URL: `/messages/<int:session_id>/`

Vue associée: `get_messages`

Description: Récupère tous les messages associés à une session de chat spécifique.

Méthode HTTP: GET

Exemple de requête curl:

```bash
curl -X GET "http://localhost:8000/messages/1/"
```

Remplacez 1 par l'ID de la session dont vous souhaitez obtenir les messages.


