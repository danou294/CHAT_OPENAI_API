import pytest
from django.urls import reverse
from rest_framework import status
from chat_sessions.models import ChatSession

@pytest.mark.django_db
def test_create_chat_session(client):
    """
    Test la création d'une nouvelle session de chat.
    """
    response = client.post(reverse('create_session'), 
                           {'participant_id': 'user123'},
                           content_type='application/json')
    assert response.status_code == status.HTTP_201_CREATED

    # Vérifie que la session a bien été créée dans la base de données
    session = ChatSession.objects.get(participant_id='user123')
    assert session is not None
    assert session.participant_id == 'user123'
    assert session.created_at is not None
