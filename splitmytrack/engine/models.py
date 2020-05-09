from django.db import models


# Create your models here.
class TrackUpload(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
