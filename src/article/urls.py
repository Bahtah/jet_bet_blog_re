from django.urls import path

from .views import *

app_name = 'article'

urlpatterns = [
    path('', list_posts, name='post_list'),
    path('detail/<slug:slug>/', detail_post, name='detail_post'),

    path('tag/<slug:tag_slug>/', tag_list, name='post_list_by_tag'),

    path('create/', create_post, name='create_post'),
    path('update/<int:pk>/', update_post, name='update_post'),
    path('delete/<int:pk>/', delete_post, name='delete_post'),

    path('category/<slug:category_slug>/', category_detail, name='category_detail'),
    path('create-category/', create_category, name='create_category'),
    path('update-category/<int:pk>/', update_category, name='update_category'),

    path('create-link/', create_link, name='create_link'),
]