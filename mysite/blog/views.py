from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

import blog
from .forms import EmailPostForm
from .models import Post


# # 포스트 목록
# def post_list(request):
#     post_list = Post.objects.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.get_page(page_number)
#     except PageNotAnInteger:
#         # page_number 이 정수가 아닌 경우 첫 번째 페이지 전달
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     return render(request,
#                   'blog/post/list.html',
#                   {'posts':posts})

# 포스트 목록 클래스
class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


# 포스트 상세 페이지
def post_detail(request, year, month, day, post):
    # SEO 개선을 위해 연, 월, 일 사용
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post':post})


# 포스트 공유
def post_share(request, post_id):
    # id로 게시물 조회
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # 폼이 제출되었다면
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ... 이메일 전송
    else:
        form = EmailPostForm()
    return render(request, 'blog/templates/post/share.html',
                  {'post': post, 'form': form})
