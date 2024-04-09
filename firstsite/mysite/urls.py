from django.urls import path, register_converter
from . import views, converters

register_converter(converters.YearMonth, 'ye4mo2da2')

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='cats')
]
