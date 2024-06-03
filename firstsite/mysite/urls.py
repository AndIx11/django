from django.urls import path, register_converter
from . import views, converters

register_converter(converters.YearMonth, 'ye4mo2da2')

urlpatterns = [
    path('', views.MySiteHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(), name='edit_page'),
    path('delete/<slug:slug>/', views.DeletePage.as_view(), name='delete_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', views.MySiteCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
]
