from django.urls import path
from findme.views.base_views import recommend_content, save_content, get_saved_content

urlpatterns = [
    path('', recommend_content, name = 'recommend_content'),
    path('Save/', save_content, name = 'save_content'),
    path('Get_Saved/<str:nickname>/', get_saved_content, name = 'get_saved_content')
]