from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from . import models


class HomePageView(TemplateView):
    template_name = 'home.html'


class PostListView(LoginRequiredMixin, ListView):
    model = models.Post
    template_name = 'posts/Post_list.html'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = models.Post
    template_name = 'posts/Post_detail.html'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.Post
    permission_required = 'blog.add_post'
    fields = ['title', 'body']
    template_name = 'posts/Post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        my_obj = self.get_object()
        return my_obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = models.Post
    template_name = 'posts/Post_delete.html'
    success_url = reverse_lazy('Post_list')


    def test_func(self):
        my_obj = self.get_object()
        return my_obj.author == self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = models.Post
    template_name = 'posts/Post_new.html'
    fields = ['title', 'body', ]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)