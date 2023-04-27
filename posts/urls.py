from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('posts/', views.PostListView.as_view(), name='Post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='Post_new'),
    path('posts/<slug:slug>/edit/',
         views.PostUpdateView.as_view(), name='Post_edit'),
     path('posts/<slug:slug>/',
         views.PostDetailView.as_view(), name='Post_detail'),
    path('posts/<slug:slug>/delete/',
         views.PostDeleteView.as_view(), name='Post_delete'),
    
]