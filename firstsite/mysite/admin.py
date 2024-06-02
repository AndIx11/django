from django.contrib import admin
from django.core.checks import messages
from django.utils.safestring import mark_safe

from .models import MySite, Category, ISBN


# Register your models here.
class ViewFilter(admin.SimpleListFilter):
    title = 'ISBN номер'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('ishave', 'Есть'),
            ('havenot', 'Отсутствует'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'ishave':
            return queryset.filter(isbn__isnull=False)
        elif self.value() == 'havenot':
            return queryset.filter(isbn__isnull=True)


@admin.register(MySite)
class MySiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [ViewFilter, 'cat__name', 'is_published']
    fields = ['title', 'slug', 'content', 'photo',
              'post_photo', 'cat', 'isbn', 'tags']
    readonly_fields = ['post_photo']
    save_on_top = True

    @admin.display(description="Изображение")
    def post_photo(self, mysite: MySite):
        if mysite.photo:
            return mark_safe(f"<img src='{mysite.photo.url}' width=50>")
        return "Без изображения"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=MySite.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=MySite.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
