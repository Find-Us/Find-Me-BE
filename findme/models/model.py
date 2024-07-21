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


# class Bookmark(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
#     content = models.JSONField()
#     created_time = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'content')
    

