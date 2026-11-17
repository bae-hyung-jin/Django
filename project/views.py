from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from project.models import Post
from django.db.models import Q  # 맨 위에 추가!

class PostLV(ListView):
    model = Post


class PostDV(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'location', 'content', 'photo']
    success_url = reverse_lazy('project:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'project/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model = Post
    fields = ['title', 'location', 'content', 'photo']
    success_url = reverse_lazy('project:index')


class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('project:index')

# project/views.py 맨 아래에 추가
class PostGalleryLV(ListView):
    model = Post
    template_name = 'project/post_gallery.html'  # 갤러리 전용 화면

    def get_queryset(self):
        # 사진(photo)이 등록된 글들만 쏙 골라오기!
        return Post.objects.filter(photo__isnull=False).exclude(photo='')

class PostLV(ListView):
    model = Post
    def get_queryset(self):
        q = self.request.GET.get('search_word', '')
        if q:
            return Post.objects.filter(
                Q(title__icontains=q) | Q(location__icontains=q) | Q(content__icontains=q)
            )
        return Post.objects.all()
