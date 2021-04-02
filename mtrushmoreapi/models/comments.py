from django.db import models


class Comment(models.Model):

    rushmore_user = models.ForeignKey("Rushmore_User", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)
    Comment = models.CharField(max_length=500)