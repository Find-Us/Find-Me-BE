from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import F


class IsOwnerOrReadOnly(BasePermission):
    """글 작성 권한 확인"""

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.author == request.user


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, type):
        model = Post if type == 'post' else Comment
        try:
            obj = model.objects.get(pk=pk)
        except model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in obj.liked_by.all():
            obj.liked_by.remove(user)
            obj.likes = F('likes') - 1
            message = f'{type.capitalize()} 섹션의 좋아요가 취소됨'
        else:
            obj.liked_by.add(user)
            obj.likes = F('likes') + 1
            message = f'{type.capitalize()} 섹션에 좋아요가 완료됨'

        obj.save()
        return Response({'message': message}, status=status.HTTP_200_OK)

