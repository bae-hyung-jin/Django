from django.contrib import admin
from walkmap.bookmark.models import Bookmark


# [2026-11-17 추가] 새 사이트 Bookmark를 /admin/ 에 등록 (목록에 id, 제목, URL 표시)
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')
