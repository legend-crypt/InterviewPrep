from django.db import models
import uuid



GENDER = [
    ("male", "male"),
    ("female", "female"),
    ("prefer_not_to_say", "prefer not to say")
]
class Profile(models.Model):
    profile_id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    other_name =  models.CharField(max_length=50)
    gender = models.CharField(choices=GENDER, max_length=50)
    contact = models.CharField(max_length=20)