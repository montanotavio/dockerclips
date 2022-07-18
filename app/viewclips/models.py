from django.db import models

# Create your models here.
class VideoClip(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=50)
    epoch = models.FloatField()
    file = models.FileField()
    filename = models.CharField(max_length=200)
    uploader = models.CharField(max_length=50, default="ADMIN")
    feed = models.BooleanField(default=True)

    def __str__(self):
        return self.title