from django.db import models

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically adds the submission timestamp

    def __str__(self):
        return f"Message from {self.name}"
