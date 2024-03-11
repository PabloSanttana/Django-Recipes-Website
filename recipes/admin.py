from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from tag.models import Tag

from .models import Category, Recipe

# Register your models here.

# colocando as tags relacoes genericas


class TagInline(GenericStackedInline):
    model = Tag
    fields = ['name']
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = ['id', 'title', 'created_at',]
    search_fields = ['id', 'title', 'description', 'preparation_steps']
    list_filter = ['category', 'author',
                   'preparation_steps_is_html', 'is_published',]
    list_per_page = 20
    list_editable = ['is_published',]
    ordering = ['-id',]

    inlines = [
        TagInline,
    ]


admin.site.register(Category, CategoryAdmin)
