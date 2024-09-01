# OpenAichat/urls.py

from django.contrib import admin
from django.urls import path
from chat_messages.views import add_message, delete_message, get_messages
from chat_sessions.views import create_session, list_sessions, delete_session

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Routes pour les sessions de chat
    path('sessions/create/', create_session, name='create_session'),
    path('sessions/', list_sessions, name='list_sessions'),
    path('sessions/<int:session_id>/delete/', delete_session, name='delete_session'),
    
    # Routes pour les messages
    path('messages/<int:session_id>/add/', add_message, name='add_message'),
    path('messages/<int:message_id>/delete/', delete_message, name='delete_message'),
    path('messages/<int:session_id>/', get_messages, name='get_messages'),  # Nouvelle route pour obtenir les messages d'une session
]
