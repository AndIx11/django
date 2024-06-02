from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=MySite.Status.PUBLISHED)


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
         'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k', 'л': 'l',
         'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's',
         'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'r',
         'ю': 'yu', 'я': 'ya'}
    return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))


class MySite(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True, verbose_name="Текст описания")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги")
    isbn = models.OneToOneField('ISBN', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='isbn', verbose_name="Номер ISBN")
    view_count = models.IntegerField(blank='True', default=0)
    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def save(self, *args, **kwargs):
        self.slug = translit_to_eng(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title


class ISBN(models.Model):
    number_13 = models.CharField(max_length=25)
    book_name = models.CharField(max_length=100)

    def __str__(self):
        return self.number_13


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag
