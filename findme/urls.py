from django.urls import path
from findme.views.base_views import recommend_content

urlpatterns = [
    path('', recommend_content, name='recommend_content'),
]