from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from mysite.forms import AddPostForm, UploadFileForm
from mysite.models import MySite, Category, TagPost, UploadFiles
import uuid

from mysite.utils import DataMixin
from users.forms import RegisterUserForm

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'addpage'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


# Create your views here.
class TagPostList(DataMixin, ListView):
    template_name = 'mysite/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return (MySite.published.filter(tags__slug=self.kwargs['tag_slug'])
                .select_related('cat'))


#def show_tag_postlist(request, tag_slug):
#    tag = get_object_or_404(TagPost, slug=tag_slug)
#    posts = tag.tags.filter(is_published=MySite.Status.PUBLISHED)
#    data = {
#        'title': f'Тег: {tag.tags}',
#        'menu': menu,
#        'posts': posts,
#        'cat_selected': None,
#    }
#    return render(request, 'mysite/index.html', context=data)


class MySiteCategory(DataMixin, ListView):
    template_name = 'mysite/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.id, )

    def get_queryset(self):
        return (MySite.published.filter(cat__slug=self.kwargs['cat_slug'])
                .select_related('cat'))


#def show_category(request, cat_slug):
#    category = get_object_or_404(Category, slug=cat_slug)
#    posts = MySite.published.filter(cat_id=category.pk)
#    data = {
#        'title': f'Рубрика: {category.name}',
#        'menu': menu,
#        'posts': posts,
#        'cat_selected': category.pk,
#    }
#    return render(request, 'mysite/index.html', context=data)


class ShowPost(DataMixin, DetailView):
    model = MySite
    template_name = 'mysite/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])

    def get_object(self, queryset=None):
        return (get_object_or_404
                (MySite.published,
                 slug=self.kwargs[self.slug_url_kwarg]))


#def show_post(request, post_slug):
#    post = get_object_or_404(MySite, slug=post_slug)
#    data = {'title': post.title,
#            'menu': menu,
#            'post': post,
#            'cat_selected': 0,
#            }
#    return render(request, 'mysite/post.html', context=data)


class MySiteHome(DataMixin, ListView):
    template_name = 'mysite/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0, )

    def get_queryset(self):
        return MySite.published.all().select_related('cat')

#def index(request):  # HttpRequest
#    posts = MySite.objects.filter(is_published=1)
#    data = {
#        'title': 'Главная страница',
#        'menu': menu,
#        'posts': MySite.published.all(),
#        'cat_selected': 0,
#    }
#    return render(request, 'mysite/index.html', context=data)


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


@login_required
def about(request):
    contact_list = MySite.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'mysite/about.html',
                  {'page_obj': page_obj, 'title': 'О сайте'})


@permission_required(perm='mysite.view_mysite', raise_exception=True)
def contact(request):
    return HttpResponse("Обратная связь")


#def addpage(request):
#    if request.method == 'POST':
#        form = AddPostForm(request.POST, request.FILES)
#        if form.is_valid():
#            form.save()
#            return redirect('home')
#    else:
#        form = AddPostForm()
#    return render(request, 'mysite/addpage.html',
#                  {'menu': menu,
#                   'title': 'Добавление статьи',
#                   'form': form})


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    model = MySite
    permission_required = 'mysite.add_mysite'
    #form_class = AddPostForm
    fields = ['title', 'slug', 'content', 'is_published', 'cat', 'isbn', 'tags']
    template_name = 'mysite/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление статьи'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
    model = MySite
    permission_required = 'mysite.change_mysite'
    fields = ['title', 'slug', 'content', 'is_published', 'cat', 'isbn', 'tags']
    template_name = 'mysite/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'


class DeletePage(PermissionRequiredMixin, DataMixin, DeleteView):
    model = MySite
    template_name = 'mysite/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление статьи'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

