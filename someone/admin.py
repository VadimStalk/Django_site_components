from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from .models import TechStr, Category

class AnalogFilter(admin.SimpleListFilter):
    title = 'Наличие аналога'
    parameter_name = 'status'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('analog_yes', 'Есть аналог'),
            ('analog_no', 'Аналог отсутствует')    
            ]
    

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'analog_yes':
            return queryset.filter(analog__isnull=False)
        elif self.value() == 'analog_no':
            return queryset.filter(analog__isnull=True)

@admin.register(TechStr)
class TechStrAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'analog'] # Поля для редактирования в режиме редактирования
    # exclude = ['tags', 'is_published'] # Исключаем поля в режиме редактирования
    readonly_fields = ['slug'] # Указать поля не для редактирования, только для чтения в режиме редактирования
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', ) # Кликабельные
    ordering = ['-time_create', 'title'] # Сортировка
    list_editable = ('is_published', ) #Изменяемые
    list_per_page = 10 # Пангинация
    actions = ['set_published', 'set_draft'] # В строке действия - выпадающий список
    search_fields = ['title__startswith', 'cat__name'] # Поиск
    list_filter = [AnalogFilter, 'cat__name', 'is_published', ] # Свой фильтр

    @admin.display(description='Краткая инфо', ordering='content')
    def brief_info(self, techstr: TechStr):
        return f"Описание {len(techstr.content)} символов"
    
    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=TechStr.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=TechStr.Status.DRAFT)
        self.message_user(request, f"Записей снятых с публикации: {count}", messages.WARNING) # messages.WARNING значет с воскл знаком перед надписью


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['id']


# admin.site.register(TechStr, TechStrAdmin)
