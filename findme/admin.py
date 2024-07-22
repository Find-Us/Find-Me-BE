from django.contrib import admin
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation,D_Movie_Recommendation, A_Book_Recommend, B_Book_Recommend, C_Book_Recommend, D_Book_Recommend, A_Song_Recommend, B_Song_Recommend, C_Song_Recommend, D_Song_Recommend


@admin.register(A_Movie_Recommendation)
class AMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

@admin.register(B_Movie_Recommendation)
class BMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

@admin.register(C_Movie_Recommendation)
class CMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

@admin.register(D_Movie_Recommendation)
class CMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')


@admin.register(A_Book_Recommend)
class ABookRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(B_Book_Recommend)
class BBookRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(C_Book_Recommend)
class CBookRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(D_Book_Recommend)
class CBookRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(A_Song_Recommend)
class ASongRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'singer')

@admin.register(B_Song_Recommend)
class BSongRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'singer')

@admin.register(C_Song_Recommend)
class CSongRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'singer')

@admin.register(D_Song_Recommend)
class CSongRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'singer')


