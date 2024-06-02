from django.contrib import admin
from django.core.checks import messages

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
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    ordering = ['-time_create', 'title']
    list_editable = ('is_published', )
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [ViewFilter, 'cat__name', 'is_published']
    fields = ['title', 'slug', 'content', 'cat', 'isbn']
    readonly_fields = ['slug']

    @admin.display(description="Краткое описание")
    def brief_info(self, women: MySite):
        return f"Описание {len(women.content)} символов."

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
