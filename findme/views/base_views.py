from rest_framework.response import Response
from rest_framework.decorators import api_view
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation, A_Book_Recommend, B_Book_Recommend, C_Book_Recommend, A_Song_Recommend, B_Song_Recommend, C_Song_Recommend
from findme.serializers import AMovieRecommendSerializer, BMovieRecommendSerializer, CMovieRecommendSerializer, ABookRecommendSerializer, BBookRecommendSerializer, CBookRecommendSerializer, ASongRecommendSerializer, BSongRecommendSerializer, CSongRecommendSerializer


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
        movies = A_Movie_Recommendation.objects.order_by('?')[:3]
        books = A_Book_Recommend.objects.order_by('?')[:3]
        songs = A_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = AMovieRecommendSerializer(movies, many=True)
        book_serializer = ABookRecommendSerializer(books, many=True)
        song_serializer = ASongRecommendSerializer(songs, many=True)

        

    elif group2_sum >= group1_sum and group2_sum >= group3_sum:
        movies = B_Movie_Recommendation.objects.order_by('?')[:3]
        books = B_Book_Recommend.objects.order_by('?')[:3]
        songs = B_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = BMovieRecommendSerializer(movies, many=True)
        book_serializer = BBookRecommendSerializer(books, many=True)
        song_serializer = BSongRecommendSerializer(songs, many=True)


    else:
        movies = C_Movie_Recommendation.objects.order_by('?')[:3]
        books = C_Book_Recommend.objects.order_by('?')[:3]
        songs = C_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = CMovieRecommendSerializer(movies, many=True)
        book_serializer = CBookRecommendSerializer(books, many=True)
        song_serializer = CSongRecommendSerializer(songs, many=True)


    

    response_data = {
        'movies' : movie_serializer.data,
        'books' : book_serializer.data,
        'songs' : song_serializer.data,
    }

    movie_serializer = AMovieRecommendSerializer(movies, many=True)
    book_serializer = ABookRecommendSerializer(books, many=True)
    song_serializer = ASongRecommendSerializer(songs, many=True)

    return Response(response_data)

