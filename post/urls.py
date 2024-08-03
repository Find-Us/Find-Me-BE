from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView, CommentDetailAPIView, LikeAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<int:pk>/like/<str:type>/', LikeAPIView.as_view(), name='like_post'),
    path('posts/<int:post_id>/comments/', CommentListCreateAPIView.as_view(), name='post_comment_list'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='post_comment_detail'),
    path('comments/<int:pk>/like/<str:type>/', LikeAPIView.as_view(), name='like_comment'),
]
