from django.contrib import admin
from django.urls import path

# Importation des vues nécessaires
from chat_messages.views import add_message, delete_message, get_messages
from chat_sessions.views import create_session, list_sessions, delete_session
from payments.views import StripeCheckoutView

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Routes pour les sessions de chat avec préfixe /api/
    path('api/sessions/create/', create_session, name='create_session'),  # Créer une nouvelle session de chat
    path('api/sessions/', list_sessions, name='list_sessions'),  # Lister toutes les sessions de chat
    path('api/sessions/<int:session_id>/delete/', delete_session, name='delete_session'),  # Supprimer une session de chat
    
    # Routes pour les messages avec préfixe /api/
    path('api/sessions/<int:session_id>/messages/add/', add_message, name='add_message'),  # Ajouter un message à une session
    path('api/messages/<int:message_id>/delete/', delete_message, name='delete_message'),  # Supprimer un message
    path('api/sessions/<int:session_id>/messages/', get_messages, name='get_messages'),  # Obtenir les messages d'une session

    # Route pour Stripe avec préfixe /api/
    path('api/create-checkout-session/', StripeCheckoutView.as_view(), name='create_checkout_session'),
]
