import uuid
from collections import defaultdict

from django.contrib.auth.models import User
# from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tag.models import Tag

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name=_('Title'))
    description = models.CharField(
        max_length=165, verbose_name=_('Description'))
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(verbose_name=_('Preparation time'))
    preparation_time_unit = models.CharField(
        max_length=65, verbose_name=_('Preparation time unit'))
    servings = models.IntegerField(verbose_name=_('Servings'))
    servings_unit = models.CharField(
        max_length=65, verbose_name=_('Servings unit'))
    preparation_steps = models.TextField(verbose_name=_('Preparation steps'))
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name=_('Preparation steps is html'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(
        default=False, verbose_name=_('Is published'))
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/',
        blank=True, default='',
        verbose_name=_('Cover')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        verbose_name=_('Category')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Author')
    )

    # usando para fazer relações generecia usando content_type
    # tags = GenericRelation(Tag, related_query_name='recipes')

    # usando o metodo mais comun
    # relações de banco de dados MayToMay

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        default="",
        verbose_name=_('Tags')
    )

    def __str__(self):
        return self.title

    def clean(self, *args, **kwargs):

        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title).first()

        if recipe_from_db:
            if self.pk != recipe_from_db.pk:
                error_messages['title'].append(
                    "Found recipes with the same title")

        if error_messages:
            raise ValidationError(error_messages)

    def save(self, *args, **kwargs):
        # Se o objeto já existe e o título foi alterado
        if self.pk:
            original = Recipe.objects.get(pk=self.pk)
            if self.title != original.title:
                self._generate_unique_slug()
        # Se for um novo objeto e não tiver slug, gera um novo
        elif not self.slug:
            self._generate_unique_slug()
        # Chama o método save() da classe pai para salvar o objeto
        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.title)
        # Obtemos os primeiros 8 caracteres do UUID
        unique_id = str(uuid.uuid4())[:16]
        self.slug = f"{base_slug}-{unique_id}"

    def get_absolute_url(self):
        return reverse("recipes:details", kwargs={"pk": self.id})

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")
