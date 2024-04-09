from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from mysite.models import MySite

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


cats_db = [
    {'id': 1, 'name': 'Новинки'},
    {'id': 2, 'name': 'Бестселлеры'},
    {'id': 3, 'name': 'Триллеры'},
    {'id': 4, 'name': 'Фантастика'},
    {'id': 5, 'name': 'Детская литература'},

]


# Create your views here.
def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': MySite.published.all(),
        'cat_selected': cat_id,
    }
    return render(request, 'mysite/index.html', context=data)


def show_post(request, post_slug):
    post = get_object_or_404(MySite, slug=post_slug)
    data = {'title': post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 0,
            }
    return render(request, 'mysite/post.html', context=data)


def index(request):  # HttpRequest
    posts = MySite.objects.filter(is_published=1)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
    }
    return render(request, 'mysite/index.html', context=data)


def about(request):
    return render(request, 'mysite/about.html',
                  {'title': 'О сайте', 'menu': menu})


def addpage(request):
    return HttpResponse("Добавление статьи")


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

