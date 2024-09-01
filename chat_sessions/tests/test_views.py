import pytest
from django.urls import reverse
from rest_framework import status
from chat_sessions.models import ChatSession

@pytest.mark.django_db
def test_create_session(client):
    """
    Test la création d'une session de chat via l'API.
    """
    response = client.post(
        reverse('create_session'),
        {'participant_id': 'user123'},
        content_type='application/json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    
    # Vérifie que la session a bien été créée dans la base de données
    session = ChatSession.objects.get(participant_id='user123')
    assert session is not None
    assert session.participant_id == 'user123'
    assert session.created_at is not None

@pytest.mark.django_db
def test_list_sessions(client):
    """
    Test la récupération de la liste des sessions de chat via l'API.
    """
    ChatSession.objects.create(participant_id="user123")
    response = client.get(reverse('list_sessions'))
    assert response.status_code == status.HTTP_200_OK
    
    # Vérifie que la réponse contient les sessions
    data = response.json()
    assert 'sessions' in data
    assert len(data['sessions']) > 0
    assert all('id' in session and 'participant_id' in session for session in data['sessions'])

@pytest.mark.django_db
def test_delete_session(client):
    """
    Test la suppression d'une session de chat via l'API.
    """
    session = ChatSession.objects.create(participant_id="user123")
    response = client.delete(reverse('delete_session', args=[session.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Vérifie que la session a été supprimée de la base de données
    assert not ChatSession.objects.filter(id=session.id).exists()
