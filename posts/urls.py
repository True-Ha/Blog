from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='Post_list'),
    path('posts/new/', views.create_post, name='Post_new'),
    path('posts/<slug:slug>/edit/',
         views.PostUpdateView.as_view(), name='Post_edit'),
     path('posts/<slug:slug>/',
         views.PostDetailView.as_view(), name='Post_detail'),
    path('posts/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='Post_delete'),
    path('posts/like/<slug:slug>', views.postLike, name='Post_like'),
    path('tags/<slug:tag_slug>/', views.TagView.as_view(), name='Post_tag'),
    path('search/', views.search, name='search'),
    
    
]

