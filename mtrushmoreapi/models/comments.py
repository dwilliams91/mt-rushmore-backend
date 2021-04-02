from django.db import models


class Comment(models.Model):
    rushmore_user = models.ForeignKey("RushmoreUser", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)