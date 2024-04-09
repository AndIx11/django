from django.db import models
from django.urls import reverse


# Create your models here.
class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=MySite.Status.PUBLISHED)


class MySite(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        ordering = ['-time_create']
        indexes = [models.Index(fields=['-time_create']),]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title
