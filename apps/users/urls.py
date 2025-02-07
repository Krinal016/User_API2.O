from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('refresh',views.refresh_access_token,name ='refresh_access_token'),
    path('create', views.create_blog, name='create_blog'),
    path('blogs', views.list_blogs, name='list_blogs'),
    path('blog/<pk>', views.search_blog, name='search_blog'),
]