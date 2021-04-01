from django.db import models
from django.contrib.auth.models import User


class RushmoreUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50)
    imageURL = models.CharField(max_length=500)