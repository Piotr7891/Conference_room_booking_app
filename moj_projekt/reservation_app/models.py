from django.db import models

# Create your models here.
class ConferenceRoom(models.Model):
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ReserveRoom(models.Model):
    room_id = models.PositiveIntegerField()
    date = models.DateTimeField()
    comments = models.TextField()
