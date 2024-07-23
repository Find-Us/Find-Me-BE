from django.db import models # 데이터 베이스 보델을 정의하고 관리하는데 사용 
from django.contrib.auth.models import User # 는 Django의 기본 사용자 모델을 가져와서 사용자 계정과 관련된 데이터를 처리할 수 있게 함 
# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User) # 게시글의 작성자 타나내기 
    title = models.CharField(max_length=200) #게시글 제목 (200자 제한 )
    content = models.TextField()#게시글 내용 (제한일단 안둠)
    created_at = models.DateTimeField(auto_now_add=True) # 날짜와 시간 설정 # 객체가 처음 생성될 때 이 필드에 현재 날짜와 시간이 자동으로 저장되도록 함 
    updated_at = models.DateTimeField(auto_now=True) # 게시글이 마지막으로 수정된 날짜와 시간을 저장 옵션으로 객체가 저장될 때마다 이 필드에 현재 날짜와 시간이 자동으로 갱신되도록 함 

    def __str__(self): 
        return self.title # 이 메서드는 객체를 문자열로 나타낼 때 어떻게 표현할지를 정의, 예를 들어 Post 객체의 경우 제목(title)을 문자열로 반환
 
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') # 이 필드는 Post 모델과의 관계를 나타내며, 댓글이 달린 게시글을 의미 #해당 게시글이 삭제될 때 이 게시글에 달린 모든 댓글도 함께 삭제되도록 함
    author = models.ForeignKey(User, on_delete=models.CASCADE) #이 필드는 User 모델과의 관계를 나타내며, 댓글 작성자를 의미함 옵션으로 작성자가 삭제될 때 이 작성자가 작성한 모든 댓글도 함께 삭제되도록 함
    content = models.TextField() # 댓글 내용 저장 
    created_at = models.DateTimeField(auto_now_add=True) # 댓글이 작성된 날짜와 시간을 저장

    def __str__(self):
        return self.content[:20]
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('Post', 'User')  # 같은 사용자가 같은 게시글에 여러 번 추천할 수 없음

    def __str__(self):
        return f'{self.User.username} likes {self.Post.Title}'