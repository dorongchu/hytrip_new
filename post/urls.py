from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 조회
    path('<int:pk>/', views.post_detail, name='post_detail'),  # 디테일
    path('new/', views.post_new, name='post_new'),  # 작성
    path('edit/<int:pk>/', views.post_edit, name='post_edit'),  # 수정
    path('remove/<int:pk>/', views.post_remove, name='post_remove'), #삭제
    path('<int:pk>/comments/new/',views.post_comment, name='post_comment'), #댓글 작성
    # path('<int:pk>/comments/<int:pk>/edit', views.comment_edit, name='comment_edit'),  # 수정
    path('comments/remove/<int:pk>/', views.comment_remove, name='comment_remove'),  # 삭제
]