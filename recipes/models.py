import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True, default=None)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

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
