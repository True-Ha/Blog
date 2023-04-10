from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('Posts/', views.PostListView.as_view(), name='Post_list'),
    path('<int:pk>/edit/',
         views.PostUpdateView.as_view(), name='Post_edit'),
    path('<int:pk>/',
         views.PostDetailView.as_view(), name='Post_detail'),
    path('<int:pk>/delete/',
         views.PostDeleteView.as_view(), name='Post_delete'),
    path('new/', views.PostCreateView.as_view(), name='Post_new'),
]