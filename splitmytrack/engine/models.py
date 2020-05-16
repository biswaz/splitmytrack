from django.db import models
from model_utils.models import StatusModel
from model_utils import Choices

from rest_framework_encrypted_lookup.serializers import EncryptedLookupSerializerMixin


# Create your models here.
class TrackUpload(StatusModel):
    UPLOAD_DIR = 'uploads/'
    STATUS = Choices('new', 'processing', 'processed', 'error')
    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=UPLOAD_DIR)

    @property
    def encrypted_id(self):
        return EncryptedLookupSerializerMixin.get_cipher().encode(self.pk)

    def __str__(self):
        return self.file.name + ' : ' + self.status
