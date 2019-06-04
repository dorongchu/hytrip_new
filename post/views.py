from email import message
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Tag, Comment
from .forms import CommentForm, PostForm

#게시판
def post_list(request):
    posts = Post.objects.all()
    q = request.GET.get('q', '')  # 키값이 'q'로 지정된 값이 없으면 None이 반환됨
    if q:  # q가 널 아니면 qs에 filter 조건 추가
        posts = posts.filter(title__icontains=q)
    return render(request, 'post/post_list.html', {
        'post_list': posts,
        'q': q,
    })

#게시글 보여주기
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    all_tag = Tag.objects.all()
    mystr = post.tagged()
    my_tag = {}
    for t in all_tag:
        my_tag[t.name] = str(mystr).find(t.name)
    return render(request, 'post/post_detail.html',
                  {'post': post, 'my_tag': my_tag})

#게시글 작성(post_write.html로 넘어감)
def post_new(request, post=None):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            item = form.save()
            # return redirect(item)
            return redirect('post:post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'post/post_write.html', {'form': form, })

#게시글 수정
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return post_new(request, post)

#게시글 삭제
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post:post_list')

#게시글에 대한 댓글 달기(post_comment.html로 넘어감)
def post_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(pk=pk)
            comment.save()
            return redirect('post:post_detail', pk)
    else:
        form = CommentForm()
    return render(request, 'post/post_comment.html', {
        'form' : form,
     })

# # 댓글 수정
# def comment_edit(request, post_pk , pk):
#     post = get_object_or_404(Post, pk=post_pk)
#     comment = get_object_or_404(Comment, pk=pk)
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST, request.FILES, instance=comment)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post:post_detail', post.pk)
#     else:
#         form = CommentForm(instance=comment)
#     return render(request, 'post/post_comment.html', {
#         'form' : form,
#      })

#댓글 삭제
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.id == request.POST.objects.get(username = request.user.get_username()):
        comment.delete()
        return redirect('post:post_detail')


