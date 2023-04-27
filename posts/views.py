from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from taggit.models import Tag
from django.template.defaultfilters import slugify

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm


from .models import *

# def pageNotFound(request, exception):
#         return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class HomePageView(TemplateView): #maybe just VIEW?
    template_name = 'home.html'


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/Post_list.html'
    queryset = Post.objects.filter(draft=False).order_by('-date')
    paginate_by = 5
    
    
 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/Post_detail.html'
     

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()

            form.instance.author = self.request.user
            form.instance.post = post
            form.save()

 
            return redirect(reverse("Post_detail", kwargs={"slug": post.slug}))
    
    
    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     context = self.get_context_data(object=self.object)
    #     ip = get_client_ip(self.request)
    #     print(ip)
    #     if IpModel.objects.filter(ip=ip).exists():
    #         print("ip already present")
    #         post_id = request.GET.get('post-id')
    #         print(post_id)
    #         post = Post.objects.get(pk=post_id)
    #         post.views.add(IpModel.objects.get(ip=ip))
    #     else:
    #         IpModel.objects.create(ip=ip)
    #         post_id = request.GET.get('post-id')
    #         post = Post.objects.get(pk=post_id)
    #         post.views.add(IpModel.objects.get(ip=ip))
    #     return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    permission_required = 'blog.add_post'
    fields = ['title', 'body']
    template_name = 'posts/Post_edit.html'
    success_url = reverse_lazy('Post_list')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
    
    def test_func(self):
        my_obj = self.get_object()
        return my_obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/Post_delete.html'
    success_url = reverse_lazy('Post_list')


    def test_func(self):
        my_obj = self.get_object()
        return my_obj.author == self.request.user


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/Post_new.html'
    fields = ['title', 'body', 'tags' ]
    prepopulated_fields = {"slug": ("title",)}
    success_url = reverse_lazy('Post_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

# def create_view(request):
#     posts = Post.objects.order_by('-date')
#     common_tags = Post.tags.most_common()[:4]
#     form = PostForm(request.POST, request.FILES)
#     if form.is_valid():
#         newpost = form.save(commit=False)
#         newpost.slug = slugify(newpost.title)
#         newpost.save()

#         form.save_m2m()
#     context = {
#         'posts': posts,
#         'common_tags': common_tags,
#         'form': form,
#     }
#     return render(request, 'posts/Post_new.html', context)

def tagged(request,slug):
     tag = get_object_or_404(Tag, slug=slug)
     posts = Post.objects.filter(tags=tag)
     context = {
         'tag': tag,
         'posts': posts,
     }

     return render(request, 'posts/Post_new.html', context)

def detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'posts/Post_detail.html', {'post':post})