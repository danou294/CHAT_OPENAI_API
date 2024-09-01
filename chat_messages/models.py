from django.db import models
from chat_sessions.models import ChatSession

class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, related_name='messages', on_delete=models.CASCADE)
    sender_id = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_from_user = models.BooleanField(default=True)
    response = models.TextField(null=True, blank=True)  # Réponse d'OpenAI
    is_sent_to_openai = models.BooleanField(default=False)  # Pour savoir si le message a été envoyé à OpenAI

    def __str__(self):
        return f"Message from {self.sender_id} at {self.timestamp}"
