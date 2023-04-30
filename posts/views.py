from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from taggit.models import Tag
from django.template.defaultfilters import slugify

from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import CommentForm, PostForm


from .models import *

class TagMixin(object):
    def get_context_data(self, **kwargs):
        context = super(TagMixin, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all
        return context

def pageNotFound(request, exception):
        return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class HomePageView(TemplateView): #maybe just VIEW?
    template_name = 'home.html'


class PostListView(LoginRequiredMixin, TagMixin, ListView):
    model = Post
    template_name = 'posts/Post_list.html'
    # queryset = Post.objects.filter(draft=False).order_by('-date')
    paginate_by = 5
    # context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(draft=False).order_by('-date')
        context['popular_posts'] = Post.objects.filter(draft=False).order_by('views')
        return context
        
    
 

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
    
    def get_like(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        #addung like count
        like_status = False
        ip = get_client_ip(request)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status = True
        else:
            like_status = False
        context['like_status'] = like_status

        return self.render_to_response(context)



    def get(self, request, slug, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if IpModel.objects.filter(ip=ip).exists():
            print("ip already present")
            post_slug = request.GET.get('slug')
            print(post_slug)
            post = Post.objects.get(slug=slug)
            post.views.add(IpModel.objects.get(ip=ip))
        else:
            IpModel.objects.create(ip=ip)
            post_slug = request.GET.get('slug')
            post = Post.objects.get(slug=post_slug)
            post.views.add(IpModel.objects.get(ip=ip))
        return self.render_to_response(context)
        # return redirect(reverse("Post_detail", kwargs={"slug": post.slug}))


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    # permission_required = 'blog.add_post'
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


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     template_name = 'posts/Post_new.html'
#     success_url = reverse_lazy('Post_list')
    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)


def create_post(request):
    posts = Post.objects.order_by('-date')
    common_tags = Post.tags.most_common()[:4]
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()

        form.save_m2m()
    context = {
        'posts': posts,
        'common_tags': common_tags,
        'form': form,
        }
    return render(request, 'posts/Post_new.html', context)



class TagView(TagMixin ,ListView):
    model = Post
    template_name = "posts/Post_list.html"
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug'))




########################################################################################################################





    

class PopularPostView(ListView):
    model = Post
    template_name = 'posts/Post_list.html'
    queryset = Post.objects.filter(draft=False).order_by('-date')
    paginate_by = 5
    context_object_name = 'posts'
    
    


########################################################################################################################


def postLike(request, slug):
    post_slug = request.GET.get('slug')
    post = Post.objects.get(slug=post_slug)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('Post_detail', kwargs={"slug": post.slug})) 
    


def search(request):


    if request.method == "POST":
        searched = request.POST['searched']
        posts = Post.objects.filter(title__contains=searched)

        return render(request, 'events/search.html', {"searched":searched, "posts":posts})
    else:
        return render(request, 'events/search.html', {})
    
    