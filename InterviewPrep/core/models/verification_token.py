from django.db import models


class VerificationToken(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=20)
    time_generated = models.DateTimeField()

    def __str__(self):
        return f"{self.email}: {self.otp}"


class PasswordVerificationToken(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=20)
    time_generated = models.DateTimeField()

    def __str__(self):
        return f"{self.email}: {self.otp}"