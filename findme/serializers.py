from rest_framework import serializers
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation, A_Book_Recommend, B_Book_Recommend, C_Book_Recommend, A_Song_Recommend, B_Song_Recommend, C_Song_Recommend

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

class ABookRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_Book_Recommend
        fields = '__all__'

class BBookRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = B_Book_Recommend
        fields = '__all__'

class CBookRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = C_Book_Recommend
        fields = '__all__'

class ASongRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_Song_Recommend
        fields = '__all__'

class BSongRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_Song_Recommend
        fields = '__all__'

class CSongRecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = A_Song_Recommend
        fields = '__all__'

