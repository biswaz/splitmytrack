from django.db import models
from django.urls import reverse
from model_utils.fields import StatusField
from model_utils.models import StatusModel
from model_utils import Choices

from rest_framework_encrypted_lookup.serializers import EncryptedLookupSerializerMixin


# Create your models here.
from splitmytrack.users.models import User


class TrackUpload(StatusModel):
    STATUS = Choices('new', 'processing', 'processed', 'error')
    CONVERSION_CHOICES = Choices('preview', 'full')
    UPLOAD_DIR = 'uploads/'

    upload_time = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=UPLOAD_DIR)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    conversion_type = StatusField(choices_name='CONVERSION_CHOICES')

    @property
    def encrypted_id(self):
        return EncryptedLookupSerializerMixin.get_cipher().encode(self.pk)

    def __str__(self):
        return self.file.name + ' : ' + self.status

    def get_absolute_url(self):
        return reverse('download', args=[self.encrypted_id])
