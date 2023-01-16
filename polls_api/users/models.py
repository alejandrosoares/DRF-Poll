from django.db import models
from django.contrib.auth.models import User as _User

class User(_User):

    def __str__(self) -> str:
        return self.username
