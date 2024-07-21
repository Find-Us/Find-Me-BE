from django.db import models


class A_Movie_Recommendation(models.Model):
    title = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='posters/A')

    def __str__(self):
        return self.title
    
class B_Movie_Recommendation(models.Model):
    title = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='posters/B')

    def __str__(self):
        return self.title
    
class C_Movie_Recommendation(models.Model):
    title = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='posters/C')

    def __str__(self):
        return self.title
    