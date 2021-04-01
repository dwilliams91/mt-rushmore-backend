from django.db import models


class Post(models.Model):

    rushmore_user = models.ForeignKey("Rushmore_User", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)
    