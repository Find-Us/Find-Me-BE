from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm

@login_required  # 이 데코레이터는 사용자가 로그인했는지 확인합니다.
def post_list(request):
    posts = Post.objects.all()  # 모든 Post 객체를 가져옵니다.
    return render(request, 'community/post_list.html', {'posts': posts})  # posts라는 컨텍스트 변수와 함께 템플릿을 렌더링합니다.

@login_required  # 로그인한 사용자만 접근할 수 있습니다.
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 특정 id의 Post 객체를 가져오거나, 객체가 없으면 404 에러를 반환합니다.
    return render(request, 'community/post_detail.html', {'post': post})  # post라는 컨텍스트 변수와 함께 템플릿을 렌더링합니다.

@login_required  # 로그인한 사용자만 접근할 수 있습니다.
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)  # POST 요청 데이터로 PostForm을 생성합니다.
        if form.is_valid():
            post = form.save(commit=False)  # 폼 데이터를 저장하되, 아직 DB에는 반영하지 않습니다.
            post.author = request.user  # 현재 로그인한 사용자를 author로 설정합니다.
            post.save()  # DB에 Post 객체를 저장합니다.
            return redirect('post_detail', post_id=post.id)  # 새로 생성된 포스트의 상세 페이지로 리디렉션합니다.
    else:
        form = PostForm()  # GET 요청 시 빈 PostForm을 생성합니다.
    return render(request, 'community/post_form.html', {'form': form})  # form이라는 컨텍스트 변수와 함께 템플릿을 렌더링합니다.

@login_required  # 로그인한 사용자만 접근할 수 있습니다.
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 특정 id의 Post 객체를 가져오거나, 객체가 없으면 404 에러를 반환합니다.
    if request.method == 'POST':
        form = CommentForm(request.POST)  # POST 요청 데이터로 CommentForm을 생성합니다.
        if form.is_valid():
            comment = form.save(commit=False)  # 폼 데이터를 저장하되, 아직 DB에는 반영하지 않습니다.
            comment.author = request.user  # 현재 로그인한 사용자를 author로 설정합니다.
            comment.post = post  # 현재 포스트를 comment의 post로 설정합니다.
            comment.save()  # DB에 Comment 객체를 저장합니다.
            return redirect('post_detail', post_id=post.id)  # 댓글이 추가된 포스트의 상세 페이지로 리디렉션합니다.
    else:
        form = CommentForm()  # GET 요청 시 빈 CommentForm을 생성합니다.
    return render(request, 'community/add_comment.html', {'form': form})  # form이라는 컨텍스트 변수와 함께 템플릿을 렌더링합니다.

@login_required  # 로그인한 사용자만 접근할 수 있습니다.
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 특정 id의 Post 객체를 가져오거나, 객체가 없으면 404 에러를 반환합니다.
    like, created = Like.objects.get_or_create(post=post, user=request.user)  # Like 객체가 없으면 생성하고, 있으면 가져옵니다.
    if not created:
        like.delete()  # 이미 좋아요를 눌렀다면, 좋아요를 취소합니다.
    return redirect('post_detail', post_id=post.id)  # 포스트의 상세 페이지로 리디렉션합니다.

@login_required  # 로그인한 사용자만 접근할 수 있습니다.
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # POST 요청 데이터와 파일로 PostForm을 생성합니다.
        if form.is_valid():
            post = form.save(commit=False)  # 폼 데이터를 저장하되, 아직 DB에는 반영하지 않습니다.
            post.author = request.user  # 현재 로그인한 사용자를 author로 설정합니다.
            post.save()  # DB에 Post 객체를 저장합니다.
            return redirect('post_detail', pk=post.pk)  # 새로 생성된 포스트의 상세 페이지로 리디렉션합니다.
    else:
        form = PostForm()  # GET 요청 시 빈 PostForm을 생성합니다.
    return render(request, 'community/post_form.html', {'form': form})  # form이라는 컨텍스트 변수와 함께 템플릿을 렌더링합니다.
