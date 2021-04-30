from django.db import models


class Post(models.Model):

    rushmore_user = models.ForeignKey("RushmoreUser", on_delete=models.CASCADE, related_name="relateduser")
    thread = models.ForeignKey("Thread", on_delete=models.CASCADE, related_name="relatedpost")
    
    @property
    def givenThread(self):
        return self.__givenThread

    @givenThread.setter 
    def givenThread(self, value):
        self.__givenThread = value