from django.urls import path
from project import views

app_name = 'project'

urlpatterns = [
    # /project/  -> 글 목록 화면
    path('', views.PostLV.as_view(), name='index'),

    # /project/1/  -> 글 상세 화면 (1번 글)
    path('<int:pk>/', views.PostDV.as_view(), name='detail'),

    # /project/add/  -> 글 작성
    path('add/', views.PostCreateView.as_view(), name="add"),

    # /project/change/  -> 내 글 관리 목록
    path('change/', views.PostChangeLV.as_view(), name="change"),

    # /project/1/update/  -> 글 수정
    path('<int:pk>/update/', views.PostUpdateView.as_view(), name="update"),

    # /project/1/delete/  -> 글 삭제
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name="delete"),

    # project/urls.py 의 urlpatterns 안에 추가
    path('gallery/', views.PostGalleryLV.as_view(), name='gallery'),
]
