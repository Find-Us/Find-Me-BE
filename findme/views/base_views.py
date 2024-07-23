from rest_framework.response import Response
from rest_framework.decorators import api_view
from findme.models.model import A_Movie_Recommendation, B_Movie_Recommendation, C_Movie_Recommendation, D_Movie_Recommendation, A_Book_Recommend, B_Book_Recommend, C_Book_Recommend,D_Book_Recommend, A_Song_Recommend, B_Song_Recommend, C_Song_Recommend, D_Song_Recommend, SavedContent
from findme.serializers import AMovieRecommendSerializer, BMovieRecommendSerializer, CMovieRecommendSerializer,DMovieRecommendSerializer, ABookRecommendSerializer, BBookRecommendSerializer, CBookRecommendSerializer,DBookRecommendSerializer, ASongRecommendSerializer, BSongRecommendSerializer, CSongRecommendSerializer, DSongRecommendSerializer, SaveContentSerializer
import random

@api_view(['POST'])
def recommend_content(request):
    scores = request.data.get('scores')

    if not scores or len(scores) != 12:
        return Response({"error" : "테스트 점수가 제대로 요청되지 않았습니다."}, status = 400)
    
    scores = list(map(int, scores))

    group_sums = {
        'A': sum([scores[2], scores[5], scores[11]]),
        'B': sum([scores[0], scores[3], scores[4]]),
        'C': sum([scores[6], scores[9], scores[10]]),
        'D': sum([scores[1], scores[7], scores[8]]),
    }

    max_score = max(group_sums.values())
    max_groups = [group for group, score in group_sums.items() if score == max_score]
    max_group = random.choice(max_groups)

    if max_group == 'A':
        return Response({"result" : "A"})

    elif max_group == 'B':
        return Response({"result" : "B"})


    elif max_group == 'C':
        return Response({"result" : "C"})
    
    else:
        return Response({"result" : "D"})

@api_view(['POST'])
def recommend_content2(request):
    max_group = request.data.get('keyword')
    content = request.data.get('content_type')

    if max_group == 'A':
        movies = A_Movie_Recommendation.objects.order_by('?')[:3]
        books = A_Book_Recommend.objects.order_by('?')[:3]
        songs = A_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = AMovieRecommendSerializer(movies, many=True)
        book_serializer = ABookRecommendSerializer(books, many=True)
        song_serializer = ASongRecommendSerializer(songs, many=True)

        

    elif max_group == 'B':
        movies = B_Movie_Recommendation.objects.order_by('?')[:3]
        books = B_Book_Recommend.objects.order_by('?')[:3]
        songs = B_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = BMovieRecommendSerializer(movies, many=True)
        book_serializer = BBookRecommendSerializer(books, many=True)
        song_serializer = BSongRecommendSerializer(songs, many=True)



    elif max_group == 'C':
        movies = C_Movie_Recommendation.objects.order_by('?')[:3]
        books = C_Book_Recommend.objects.order_by('?')[:3]
        songs = C_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = CMovieRecommendSerializer(movies, many=True)
        book_serializer = CBookRecommendSerializer(books, many=True)
        song_serializer = CSongRecommendSerializer(songs, many=True)

    
    else:
        movies = D_Movie_Recommendation.objects.order_by('?')[:3]
        books = D_Book_Recommend.objects.order_by('?')[:3]
        songs = D_Song_Recommend.objects.order_by('?')[:3]
        movie_serializer = DMovieRecommendSerializer(movies, many=True)
        book_serializer = DBookRecommendSerializer(books, many=True)
        song_serializer = DSongRecommendSerializer(songs, many=True)


    if content == 'movie':
        response_data = {
            'movies' : movie_serializer.data,
        }
    elif content == 'book':
        response_data = {
            'books' : book_serializer.data,
        }
    elif content == 'song':
        response_data = {
            'songs' : book_serializer.data,
        }
    else:
        response_data = {
            'movies' : movie_serializer.data,
            'books' : book_serializer.data,
            'songs' : song_serializer.data,
        }

    return Response(response_data)


@api_view(['POST'])
def save_content(request):
    data = request.data
    serializer = SaveContentSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Content saved successfullt"}, status = 201)
    else:
        return Response(serializer.errors, status = 400)
    
@api_view(['GET'])
def get_saved_content(request, nickname):
    saved_contents = SavedContent.objects.filter(nickname = nickname)
    serializer = SaveContentSerializer(saved_contents, many = True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_saved_content(request):
    nickname = request.data.get('nickname')
    title = request.data.get('title')

    if not nickname or not title:
        return Response({"error": "올바른 요청이 아닙니다."}, status = 400)

    try:
        saved_content = SavedContent.objects.get(nickname=nickname, title = title)
        saved_content.delete()
        return Response({"message": "해당 컨텐츠를 삭제하였습니다."}, status = 200)
    except SavedContent.DoesNotExist:
        return Response({"error": "컨텐츠를 찾을 수 없습니다."}, status = 404)

