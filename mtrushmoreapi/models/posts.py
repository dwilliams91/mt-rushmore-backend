from django.db import models


class Post(models.Model):

    rushmore_user = models.ForeignKey("RushmoreUser", on_delete=models.CASCADE)
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE)
    
    @property
    def givenThread(self):
        return self.__joined

    @givenThread.setter 
    def joined(self, value):
        self.__joined = value