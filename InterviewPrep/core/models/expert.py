from django.db import models
from core.models.accounts import UserAccount
import uuid


class Expert(models.Model):
    expert_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    work_email = models.EmailField( max_length=254)
    id_no = models.CharField(max_length=50)
    id_picture = models.ImageField(upload_to="id-picture/")
    selfie = models.ImageField(upload_to="selfie/")