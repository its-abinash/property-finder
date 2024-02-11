import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model. Here, password and email are required. Other fields are optional.
    """
    full_name = models.CharField(('full name'), max_length=30, blank=True)
    contact_number = models.CharField(max_length=30, db_index=True)
    is_contact_number_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    email = models.EmailField(('email address'), blank=True, db_index=True)

    def save(self, *args, **kwargs):
        if self.username is None or len(self.username) == 0:
            self.username = str(uuid.uuid4().hex)[:30]

        self.full_name = self.first_name + " " + self.last_name
        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)
