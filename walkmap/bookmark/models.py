from django.db import models
from django.contrib.auth.models import User


# [2026-11-17 추가] 새 사이트용 Bookmark 모델 (원래 bookmark/models.py 복사본).
# 앱 label이 wm_bookmark라서 DB 테이블은 wm_bookmark_bookmark로 따로 생긴다. (원래 데이터와 섞이지 않음)
class Bookmark(models.Model):
    title = models.CharField('TITLE', max_length=100, blank=True)
    url = models.URLField('URL', unique=True)
    # [수정] related_name 추가: 원래 bookmark 앱의 Bookmark도 User를 가리키는데,
    # 이름이 같으면 User.bookmark_set 이 겹쳐서 check 에러가 나므로 다르게 지정한다.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='OWNER',
                              blank=True, null=True, related_name='wm_bookmarks')

    def __str__(self):
        return self.title

    # 제목을 비워 두면 URL을 제목으로 사용
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.url
        super().save(*args, **kwargs)
