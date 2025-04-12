from django.db import models

class Leader(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    values = models.TextField()
    image = models.ImageField(upload_to='leaders/', blank=True, null=True)

    def __str__(self):
        return self.name
