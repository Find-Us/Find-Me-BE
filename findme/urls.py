from django.urls import path
from findme.views.base_views import recommend_content,recommend_content2, save_content, get_saved_content, delete_saved_content

urlpatterns = [
    path('', recommend_content, name = 'recommend_content'),
    path('Content', recommend_content2, name = 'recommend_content2'),
    path('Save/', save_content, name = 'save_content'),
    path('Get_Saved/<str:nickname>/', get_saved_content, name = 'get_saved_content'),
    path('Delete/', delete_saved_content, name = 'delete_saved_content')
]