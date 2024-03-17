import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify

# Create your models here.


# codigo para models generico
class TagGeneric(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    # aqui começam as campo para a relacao genericas
    # Representa o model que queremos encaixar aqui
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    # representacao da linha do model
    object_id = models.CharField(max_length=255)

    # Um campo que representa a relacao generica que conhece os
    # campos acima (content_type,object_id)

    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # verificando se já tem id
        if self.pk:
            original = Tag.objects.get(pk=self.pk)

            if self.name != original.name:
                self._generate_unique_slug()

        elif not self.slug:
            self._generate_unique_slug()

        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)

        unique_id = str(uuid.uuid4())[:16]
        self.slug = f'{base_slug}-{unique_id}'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # verificando se já tem id
        if self.pk:
            original = Tag.objects.get(pk=self.pk)

            if self.name != original.name:
                self._generate_unique_slug()

        elif not self.slug:
            self._generate_unique_slug()

        super().save(*args, **kwargs)

    def _generate_unique_slug(self):
        base_slug = slugify(self.name)

        unique_id = str(uuid.uuid4())[:16]
        self.slug = f'{base_slug}-{unique_id}'
