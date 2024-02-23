def recipe_dict(recipe):

    return {
        'id': recipe.id,
        'title': recipe.title,
        'description': recipe.description,
        'preparation_time': recipe.preparation_time,
        'preparation_time_unit': recipe.preparation_time_unit,
        'servings': recipe.servings,
        'servings_unit': recipe.servings_unit,
        'preparation_steps': recipe.preparation_steps,
        'created_at': str(recipe.created_at),
        'updated_at': str(recipe.updated_at),
        'author': {
            # flake8: noqa E501
            'username': recipe.author.username if recipe.author.username else "",
            'first_name': recipe.author.first_name if recipe.author.first_name else "",
            'last_name': recipe.author.last_name if recipe.author.last_name else "",
        },
        'category': {
            'name': str(recipe.category),
            'id': recipe.category.id
        },
        'cover': {
            'url': recipe.cover.url if recipe.cover else "",
        }
    }
