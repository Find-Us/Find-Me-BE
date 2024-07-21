from rest_framework.response import Response
from rest_framework.decorators import api_view
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation
from findme.serializers import AMovieRecommendSerializer, BMovieRecommendSerializer, CMovieRecommendSerializer

@api_view(['POST'])
def recommend_content(request):
    scores = request.data.get('scores')

    if not scores or len(scores) != 9:
        return Response({scores}, status = 400)
    
    scores = list(map(int, scores))

    group1_sum = sum(scores[:3])
    group2_sum = sum(scores[3:6])
    group3_sum = sum(scores[6:])

    if group1_sum >= group2_sum and group1_sum >= group3_sum:
        movies = A_Movie_Recommendation.objects.all()
        serializer = AMovieRecommendSerializer(movies, many =True)
    elif group2_sum >= group1_sum and group2_sum >= group3_sum:
        movies = B_Movie_Recommendation.objects.all()
        serializer = BMovieRecommendSerializer(movies, many = True)
    else:
        movies = C_Movie_Recommendation.objects.all()
        serializer = CMovieRecommendSerializer(movies, many=True)

    return Response(serializer.data)

