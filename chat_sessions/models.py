from django.db import models

class ChatSession(models.Model):
    participant_id = models.CharField(max_length=255)
    title = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Session {self.id} with {self.participant_id}"
