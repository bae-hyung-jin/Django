from django.db import models
from django.contrib.auth.models import User

# 산책 후기 및 안전 코스 공유 모델
class Post(models.Model):
    title = models.CharField('코스 이름 / 제목', max_length=100)
    location = models.CharField('위치 / 장소', max_length=100, blank=True)
    content = models.TextField('산책 후기 / 안내')
    photo = models.ImageField('코스 사진', upload_to='project/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField('작성일', auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자', blank=True, null=True, related_name='project_posts')

    class Meta:
        ordering = ['-created_at']  # 최신 글이 제일 위에 오도록 정렬

    def __str__(self):
        return self.title
