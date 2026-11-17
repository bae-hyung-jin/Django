from django.urls import path, include

from walkmap import views

# [2026-11-17 추가] 새 사이트(walkmap)의 주소 모음.
# 앱 이름표(namespace). 템플릿에서 {% url 'walkmap:home' %} 처럼 쓴다.
app_name = 'walkmap'

urlpatterns = [
    # /walkmap/  → 새 사이트 홈(소개 화면)
    path('', views.WalkmapHomeView.as_view(), name='home'),
    # /walkmap/bookmark/  → 새 사이트 Bookmark (walkmap/bookmark/urls.py 가 처리)
    path('bookmark/', include('walkmap.bookmark.urls')),
    # /walkmap/map/  → 새 사이트 지도 (walkmap/map/urls.py 가 처리)
    path('map/', include('walkmap.map.urls')),
]
