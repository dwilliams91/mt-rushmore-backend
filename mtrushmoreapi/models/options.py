from django.db import models


class Option(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    option = models.CharField(max_length=250)
    weight = models.IntegerField() 