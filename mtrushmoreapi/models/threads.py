from django.db import models


class Thread(models.Model):

    rushmore_user = models.ForeignKey("RushmoreUser", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    