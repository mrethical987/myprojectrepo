from django.contrib import admin
from django.urls import path , include
from . import views
from blog import views
from django.urls import path, include, re_path


urlpatterns = [
    
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),    
    path('', views.blogHome, name='blogHome'),
    path('blog', views.blogHome, name='blogHome'),
    path('postComment', views.postComment, name='postComment'),
    path('<str:slug>', views.blogPost, name='blogPost'),

    

]
