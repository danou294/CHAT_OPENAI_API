import pytest
from django.urls import reverse
from chat_messages.models import Message
from chat_sessions.models import ChatSession
from rest_framework import status
import json

@pytest.mark.django_db
def test_add_message(client):
    """
    Test l'ajout d'un message à une session de chat.
    """
    # Création d'une session de chat
    session = ChatSession.objects.create(participant_id="user123")
    
    # Envoi d'une requête POST pour ajouter un message
    response = client.post(reverse('add_message', args=[session.id]), {
        'content': 'Hello, world!',
        'sender_id': 'user123',
        'is_from_user': True
    }, content_type='application/json')
    
    # Vérifications
    assert response.status_code == status.HTTP_201_CREATED
    assert Message.objects.filter(chat_session=session, content='Hello, world!').exists()
    
    # Vérifie la réponse JSON
    response_data = response.json()
    assert response_data['message'] == f'Le message a été ajouté avec succès dans la session {session.id}.'

@pytest.mark.django_db
def test_delete_message(client):
    """
    Test la suppression d'un message existant.
    """
    # Création d'une session de chat
    session = ChatSession.objects.create(participant_id="user123")
    
    # Création d'un message
    message = Message.objects.create(chat_session=session, sender_id="user123", content="Hello", is_from_user=True)
    
    # Envoi d'une requête DELETE pour supprimer le message
    response = client.delete(reverse('delete_message', args=[message.id]))
    
    # Vérifications
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Message.objects.filter(id=message.id).exists()

@pytest.mark.django_db
def test_get_messages(client):
    """
    Test la récupération des messages d'une session de chat.
    """
    # Création d'une session de chat
    session = ChatSession.objects.create(participant_id="user123")
    
    # Création de messages
    Message.objects.create(chat_session=session, sender_id="user123", content="Hello", is_from_user=True)
    Message.objects.create(chat_session=session, sender_id="user456", content="Hi there", is_from_user=False)
    
    # Envoi d'une requête GET pour récupérer les messages
    response = client.get(reverse('get_messages', args=[session.id]))
    
    # Vérifications
    assert response.status_code == status.HTTP_200_OK
    messages = response.json()['messages']
    
    assert len(messages) == 2
    assert any(message['content'] == "Hello" for message in messages)
    assert any(message['content'] == "Hi there" for message in messages)
