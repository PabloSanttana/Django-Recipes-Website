
from collections import defaultdict

from rest_framework import serializers

from recipes.models import Recipe
from tag.models import Tag
from utils.django_forms import is_positive_number


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # criar um dicionario dinamico para armazenar os errors de uma vez
        self.__my_errors = defaultdict(list)

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'description',
            'author',
            'category',
            'tags',
            'preparation',
            'preparation_time',
            'preparation_time_unit',
            'servings',
            'servings_unit',
            'preparation_steps',
            'public',
            'cover',
            'tag_objects',
            'tags_links',
        ]

    public = serializers.BooleanField(source='is_published', read_only=True,)
    preparation = serializers.SerializerMethodField(
        read_only=True,
    )
    # campos chave estrangeira
    category = serializers.StringRelatedField(
        read_only=True,
    )

    # isso cria uma array
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )
    tag_objects = TagSerializer(
        many=True,
        source='tags',
        read_only=True,
    )
    tags_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # Removendo por causa do read_only=True
        # queryset=Tag.objects.all(),
        view_name='recipes:recipes_tag_api_v2',
        read_only=True,
    )

    def get_preparation(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'

    def validate(self, attrs):

        if self.instance is not None:
            if attrs.get('description') is None:
                attrs['description'] = self.instance.description

            if attrs.get('preparation_time') is None:
                attrs['preparation_time'] = self.instance.preparation_time

            if attrs.get('servings') is None:
                attrs['servings'] = self.instance.servings

            if attrs.get('category') is None and self.initial_data.get('category') is None:
                self.initial_data['category'] = self.instance.category

        super_validate = super().validate(attrs)

        cleaned_data = attrs

        # Verifica se a descrição tem pelo menos 5 caracteres
        if len(cleaned_data.get('description', '')) < 5:
            self.__my_errors['description'].append(
                'Description must have at least 5 characters.')

        # Verifica se o tempo de preparo é um número positivo
        if not is_positive_number(cleaned_data.get('preparation_time', 0)):
            self.__my_errors['preparation_time'].append(
                'Preparation time must be a positive number.')

        # Verifica se o número de porções é um número positivo
        if not is_positive_number(cleaned_data.get('servings', 0)):
            self.__my_errors['servings'].append(
                'Servings must be a positive number.')

        # Verifica se a categoria está presente
        if not self.initial_data.get('category'):
            self.__my_errors['category'].append(
                'Category is required.')

        # Se houver erros, lança uma exceção de validação
        if self.__my_errors:
            raise serializers.ValidationError(self.__my_errors)

        return super_validate

    def validate_title(self, value):
        title = value
        print("title", value)

        # Verifica se o título tem pelo menos 5 caracteres
        if len(title) < 5:
            self.__my_errors['title'].append(
                'Title must have at least 5 characters.')

        return title

    def validate_cover(self, value):

        # Define the maximum file size in bytes
        max_size_bytes = 2 * 1024 * 1024  # 2MB
        allowed_extensions = ['jpg', 'jpeg', 'png']

        cover = value

        # Verifica se a imagem de nao capa está presente
        if not cover:
            self.__my_errors['cover'].append(
                'Cover image is required.')

        else:
            file_extension = cover.name.split('.')[-1].lower()

            if file_extension not in allowed_extensions:
                self.__my_errors['cover'].append(
                    'Only JPG, JPEG, and PNG files are allowed')

            if cover.size > max_size_bytes:
                self.__my_errors['cover'].append(
                    'Cover image should not exceed 2MB')

        return cover

    def save(self, **kwargs):
        return super().save(**kwargs)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
