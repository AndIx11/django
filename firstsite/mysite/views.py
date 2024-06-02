from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound

from mysite.forms import AddPostForm, UploadFileForm
from mysite.models import MySite, Category, TagPost, UploadFiles
import uuid

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# Create your views here.
def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=MySite.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tags}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'mysite/index.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = MySite.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
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
        'posts': MySite.published.all(),
        'cat_selected': 0,
    }
    return render(request, 'mysite/index.html', context=data)


def handle_uploaded_file(f):
    name = f.name
    ext = ''

    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'mysite/about.html',
                  {'title': 'О сайте',
                   'menu': menu, 'form': form})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'mysite/addpage.html',
                  {'menu': menu,
                   'title': 'Добавление статьи',
                   'form': form})


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

