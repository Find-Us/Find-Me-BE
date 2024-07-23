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
    
class D_Movie_Recommendation(models.Model):
    title = models.CharField(max_length=200)
    actors = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='posters/D')

    def __str__(self):
        return self.title
    
class A_Book_Recommend(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='books/A')

    def __str__(self):
        return self.title
    
class B_Book_Recommend(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='books/B')

    def __str__(self):
        return self.title
    
class C_Book_Recommend(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='books/C')

    def __str__(self):
        return self.title
    
class D_Book_Recommend(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)
    description = models.TextField()
    image = models.ImageField(upload_to='books/D')

    def __str__(self):
        return self.title

class A_Song_Recommend(models.Model):
    title = models.CharField(max_length=300)
    singer = models.CharField(max_length=300)
    image = models.ImageField(upload_to='songs/A')

    def __str__(self):
        return self.title

class B_Song_Recommend(models.Model):
    title = models.CharField(max_length=300)
    singer = models.CharField(max_length=300)
    image = models.ImageField(upload_to='songs/B')

    def __str__(self):
        return self.title


class C_Song_Recommend(models.Model):
    title = models.CharField(max_length=300)
    singer = models.CharField(max_length=300)
    image = models.ImageField(upload_to='songs/C')

    def __str__(self):
        return self.title


class D_Song_Recommend(models.Model):
    title = models.CharField(max_length=300)
    singer = models.CharField(max_length=300)
    image = models.ImageField(upload_to='songs/D')

    def __str__(self):
        return self.title

class SavedContent(models.Model):
    nickname = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50)
    title = models.CharField(max_length=300)
    actors = models.CharField(max_length=500, blank=True, null=True)
    author = models.CharField(max_length=300, blank=True, null=True)
    singer = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.nickname} - {self.title}'

