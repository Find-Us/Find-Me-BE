from django.contrib import admin
from .models import Post, Comment

# Post 모델을 관리자 인터페이스에 등록
admin.site.register(Post)

# Comment 모델을 관리자 인터페이스에 등록
admin.site.register(Comment)