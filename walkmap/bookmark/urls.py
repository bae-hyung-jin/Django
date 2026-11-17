from django.urls import path
from walkmap.bookmark import views

# [2026-11-17 추가] 새 사이트 Bookmark 주소 (원래 bookmark/urls.py 복사본).
# /walkmap/bookmark/ 아래 주소를 담당한다. (walkmap/urls.py 에서 include)
# 앱 이름표는 'wm_bookmark'. walkmap/urls.py 안에 들어 있어서 앞에 walkmap: 이 붙는다.
# → 템플릿에서 {% url 'walkmap:wm_bookmark:index' %} 처럼 쓴다.
app_name = 'wm_bookmark'

urlpatterns = [
    path('', views.BookmarkLV.as_view(), name='index'),                           # /walkmap/bookmark/
    path('<int:pk>/', views.BookmarkDV.as_view(), name='detail'),                 # /walkmap/bookmark/3/
    path('add/', views.BookmarkCreateView.as_view(), name='add'),                 # /walkmap/bookmark/add/
    path('change/', views.BookmarkChangeLV.as_view(), name='change'),             # /walkmap/bookmark/change/
    path('<int:pk>/update/', views.BookmarkUpdateView.as_view(), name='update'),  # /walkmap/bookmark/3/update/
    path('<int:pk>/delete/', views.BookmarkDeleteView.as_view(), name='delete'),  # /walkmap/bookmark/3/delete/
]
