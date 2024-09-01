import pytest
from chat_messages.models import Message
from chat_sessions.models import ChatSession

@pytest.mark.django_db
def test_create_message():
    """
    Test la création d'un message associé à une session de chat.
    """
    # Création d'une session de chat
    session = ChatSession.objects.create(participant_id="user123")
    
    # Création d'un message
    message = Message.objects.create(
        chat_session=session,
        sender_id="user123",
        content="Hello",
        is_from_user=True
    )
    
    # Vérifications
    assert message.id is not None
    assert message.chat_session == session
    assert message.sender_id == "user123"
    assert message.content == "Hello"
    assert message.is_from_user is True
    assert message.timestamp is not None  # Assure que le timestamp est automatiquement défini
