from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from mysite.views import OwnerOnlyMixin  # "본인 것만 수정/삭제" 검사 (원래 사이트와 공유)
from walkmap.bookmark.models import Bookmark

# [2026-11-17 추가] 새 사이트용 Bookmark 뷰 (원래 bookmark/views.py 복사본).
# 바뀐 점 두 가지:
#  1) template_name 을 직접 지정 → 새 틀(walkmap/base.html)을 쓰는 walkmap/bookmark/*.html 사용
#  2) success_url 이름을 'walkmap:wm_bookmark:index' 로 변경 (원래 앱 'bookmark:index' 와 구분)
TPL = 'walkmap/bookmark/'


class BookmarkLV(ListView):  # 목록
    model = Bookmark
    template_name = TPL + 'bookmark_list.html'


class BookmarkDV(DetailView):  # 상세
    model = Bookmark
    template_name = TPL + 'bookmark_detail.html'


class BookmarkCreateView(LoginRequiredMixin, CreateView):  # 추가 (로그인 필요)
    model = Bookmark
    fields = ['title', 'url']
    template_name = TPL + 'bookmark_form.html'
    success_url = reverse_lazy('walkmap:wm_bookmark:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # 작성자를 로그인한 사용자로 저장
        return super().form_valid(form)


class BookmarkChangeLV(LoginRequiredMixin, ListView):  # 내 북마크 관리 목록
    model = Bookmark
    template_name = TPL + 'bookmark_change_list.html'

    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)


class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):  # 수정 (본인만)
    model = Bookmark
    fields = ['title', 'url']
    template_name = TPL + 'bookmark_form.html'
    success_url = reverse_lazy('walkmap:wm_bookmark:index')


class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):  # 삭제 (본인만)
    model = Bookmark
    template_name = TPL + 'bookmark_confirm_delete.html'
    success_url = reverse_lazy('walkmap:wm_bookmark:index')
