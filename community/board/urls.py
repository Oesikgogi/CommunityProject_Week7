from django.urls import path
from . import views
from .views import *

app_name = 'board'

urlpatterns = [
    path('', post_list),
    path('post/create/', post_list),
    path('post/detail/<int:pk>/', post_detail),
    path('post/update/<int:pk>/', post_detail),
    path('post/delete/<int:pk>/', post_detail),
    path('comment/create/<int:post_id>/', create_comment),
    path('comment/list/<int:post_id>/', get_comments),
]