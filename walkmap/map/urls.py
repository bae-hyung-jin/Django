from django.urls import path
from walkmap.map import views

# [2026-11-17 추가] 새 사이트 지도 주소. walkmap/urls.py 에서 'map/' 아래로 include 된다.
# 앱 이름표는 'map'. walkmap: 안에 들어 있어서 템플릿에서는 {% url 'walkmap:map:index' %} 로 쓴다.
# (walkmap/base.html 메뉴의 Map 링크가 이 이름을 사용)
app_name = 'map'

urlpatterns = [
    path('', views.MapView.as_view(), name='index'),  # /walkmap/map/
]
