import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from model_utils.models import StatusModel
from model_utils import Choices


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    coins = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class Order(StatusModel):
    STATUS = Choices('created', 'attempted', 'paid')
    buyer = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    coins = models.PositiveIntegerField()  # remove this?
    amount = models.PositiveIntegerField()
    receipt = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    razorpay_order_id = models.CharField(max_length=128, unique=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=128, null=True)
    razorpay_signature = models.CharField(max_length=128, null=True)

