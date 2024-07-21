from django.contrib import admin
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation


@admin.register(A_Movie_Recommendation)
class AMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

@admin.register(B_Movie_Recommendation)
class BMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

@admin.register(C_Movie_Recommendation)
class CMovieRecommendAdmin(admin.ModelAdmin):
    list_display = ('title', 'actors')

