from rest_framework import serializers
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation

class AMovieRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_Movie_Recommendation
        fields = '__all__'

class BMovieRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_Movie_Recommendation
        fields = '__all__'

class CMovieRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = C_Movie_Recommendation
        fields = '__all__'