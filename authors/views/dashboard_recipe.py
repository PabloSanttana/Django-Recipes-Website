from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms import RecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch')
class DashboardRecipe(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None

        if id:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                pk=id
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def renderView(self, form):
        return render(self.request, 'authors/views/dashboard_recipe_form.html',
                      {
                          'form': form,
                          'form_id': 'form_recipe',

                      })

    # metodo get, mostra um formulario vazio para uma nova receita
    # ou mostra um receita para edicao

    def get(self, request, id=None):

        recipe = self.get_recipe(id)

        form = RecipeForm(instance=recipe)

        return self.renderView(form)

    def post(self, request, id=None):

        recipe = self.get_recipe(id)

        form = RecipeForm(data=request.POST,
                          files=request.FILES,
                          instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Recipe edited successfully')

            return redirect(reverse('authors:dashboard_recipe_edit',
                                    args=(recipe.id,)))

        return self.renderView(form)


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        id = self.request.POST.get('id')
        recipe = self.get_recipe(id)
        recipe.delete()
        messages.success(self.request, 'Delete Recipe successfully')

        return redirect('authors:dashboard')
