from django.apps import AppConfig


# [2026-11-17 추가] 새 사이트(walkmap)용 bookmark 복사본의 설정.
# 원래 bookmark 앱과 겹치지 않도록 label(앱 이름표)을 'wm_bookmark'로 새로 지었다.
#  - name : 파이썬 경로 (walkmap/bookmark 폴더)
#  - label: Django 내부 이름표. DB 테이블 이름(wm_bookmark_bookmark)과 마이그레이션에 쓰인다.
class WmBookmarkConfig(AppConfig):
    name = 'walkmap.bookmark'
    label = 'wm_bookmark'
