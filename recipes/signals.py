
import os

from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

from recipes.models import Recipe

# Create your models here.


def delete_cover(instance):
    try:
        os.remove(instance.cover.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(pre_save, sender=Recipe)
def recipe_cover_update(sender, instance, *args, **kwargs):
    if instance.pk:
        old_recipe = Recipe.objects.get(pk=instance.pk)
        is_new_cover = old_recipe.cover != instance.cover
        if is_new_cover:
            delete_cover(old_recipe)


@receiver(pre_delete, sender=Recipe)
def recipe_cover_delete(sender, instance, *args, **kwargs):
    old_recipe = Recipe.objects.get(pk=instance.pk)
    delete_cover(old_recipe)
