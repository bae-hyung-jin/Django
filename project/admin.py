from django.contrib import admin
from project.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'created_at')  # 관리자 화면에 보일 열(Column)들