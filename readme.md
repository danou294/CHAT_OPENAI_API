# 🚀 CodeSphere Backend API

**API Django pour la plateforme CodeSphere**

Backend Django qui fournit les APIs nécessaires pour l'éditeur de code, le chatbot IA, et le système de paiement de CodeSphere.

## ✨ Fonctionnalités

### 🤖 **Chatbot IA**
- **Intégration OpenAI** pour les réponses intelligentes
- **Gestion des conversations** avec historique
- **Génération automatique** de titres de conversations
- **Support multi-températures** pour les réponses

### 💳 **Système de Paiement**
- **Intégration Stripe** pour les paiements sécurisés
- **Gestion des sessions** de checkout
- **Webhooks** pour la validation des paiements

### 🔐 **Authentification**
- **CORS configuré** pour le frontend React
- **Gestion des sessions** utilisateur
- **Sécurité** avec tokens d'authentification

## 🛠️ Installation

### Prérequis
- **Python 3.8+**
- **pip** ou **pipenv**
- **Compte OpenAI** (pour l'IA)
- **Compte Stripe** (pour les paiements)

### 1. Cloner le projet
```bash
git clone https://github.com/danou294/CodeSphere.git
cd CHAT_OPENAI_API
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration des variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your_openai_api_key_here

# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_TEST_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_PRICE_ID=price_your_stripe_price_id

# Django Configuration
DEBUG=True
SECRET_KEY=your_django_secret_key_here

# Database (optionnel - SQLite par défaut)
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Migrations de la base de données
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

### 7. Démarrer le serveur
```bash
python manage.py runserver
```

L'API sera accessible sur `http://localhost:8000`

## 🏗️ Architecture

### **Structure du Projet**
```
CHAT_OPENAI_API/
├── chat_messages/        # Gestion des messages IA
│   ├── models.py        # Modèle Message
│   ├── views.py         # API endpoints pour les messages
│   └── migrations/      # Migrations de base de données
├── chat_sessions/       # Gestion des conversations
│   ├── models.py        # Modèle ChatSession
│   ├── views.py         # API endpoints pour les sessions
│   └── migrations/      # Migrations de base de données
├── payments/            # Système de paiement Stripe
│   ├── models.py        # Modèles de paiement
│   ├── views.py         # API endpoints Stripe
│   └── migrations/      # Migrations de base de données
├── OpenAichat/          # Configuration Django
│   ├── settings.py      # Paramètres Django
│   ├── urls.py          # Routage des URLs
│   └── wsgi.py          # Configuration WSGI
└── manage.py            # Script de gestion Django
```

### **Technologies Utilisées**
- **Django 4.2** - Framework web Python
- **OpenAI API** - Intelligence artificielle
- **Stripe** - Paiements en ligne
- **SQLite** - Base de données (par défaut)
- **CORS** - Cross-Origin Resource Sharing
- **Django REST** - APIs REST

## 📡 Endpoints API

### **Chat Sessions**
```
GET    /api/sessions/                    # Lister les sessions
POST   /api/sessions/create/             # Créer une session
POST   /api/conversations/create/        # Créer conversation + message
DELETE /api/sessions/{id}/delete/        # Supprimer une session
```

### **Messages**
```
GET    /api/sessions/{id}/messages/      # Obtenir les messages
POST   /api/sessions/{id}/messages/add/ # Ajouter un message
DELETE /api/messages/{id}/delete/        # Supprimer un message
```

### **Paiements**
```
POST   /api/create-checkout-session/    # Créer session Stripe
```

## 🔧 Scripts Disponibles

```bash
# Développement
python manage.py runserver              # Serveur de développement
python manage.py runserver 0.0.0.0:8000 # Serveur accessible depuis l'extérieur

# Base de données
python manage.py makemigrations         # Créer les migrations
python manage.py migrate               # Appliquer les migrations
python manage.py migrate --fake-initial # Migrations initiales

# Administration
python manage.py createsuperuser       # Créer un superutilisateur
python manage.py shell                 # Shell Django interactif

# Tests
python manage.py test                  # Lancer les tests
```

## 🐳 Déploiement avec Docker

### **Docker Compose**
```bash
# Construire et démarrer les services
docker-compose up --build

# Démarrer en arrière-plan
docker-compose up -d

# Arrêter les services
docker-compose down
```

### **Configuration Docker**
- **Django** sur le port 8000
- **Nginx** sur le port 80 (reverse proxy)
- **Volume** pour la base de données SQLite

## 🔒 Sécurité

### **Configuration CORS**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Frontend React
    "http://localhost:3001",  # Frontend React (port alternatif)
]
```

### **Variables d'environnement**
- Toutes les clés sensibles sont dans `.env`
- `.env` est dans `.gitignore`
- Utilisation de `python-decouple` pour la gestion

## 📊 Base de Données

### **Modèles Principaux**

#### **ChatSession**
```python
- id: Primary Key
- participant_id: CharField (ID utilisateur)
- title: CharField (Titre de la conversation)
- created_at: DateTimeField
```

#### **Message**
```python
- id: Primary Key
- chat_session: ForeignKey vers ChatSession
- sender_id: CharField (ID expéditeur)
- content: TextField (Contenu du message)
- is_from_user: BooleanField
- is_sent_to_openai: BooleanField
- message_response: TextField (Réponse IA)
- timestamp: DateTimeField
```

## 🚀 Déploiement en Production

### **Variables d'environnement de production**
```env
DEBUG=False
SECRET_KEY=your_production_secret_key
OPENAI_API_KEY=sk-your_production_openai_key
STRIPE_SECRET_KEY=sk_live_your_live_stripe_key
DATABASE_URL=postgresql://user:pass@host:port/db
```

### **Serveur Web**
- **Gunicorn** pour servir Django
- **Nginx** comme reverse proxy
- **PostgreSQL** pour la base de données

## 🤝 Contribution

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues** : [GitHub Issues](https://github.com/danou294/CodeSphere/issues)
- **Email** : danielevy29@gmail.com

---

**Fait avec ❤️ en France** 🇫🇷

*CodeSphere Backend - API puissante pour votre plateforme de développement*