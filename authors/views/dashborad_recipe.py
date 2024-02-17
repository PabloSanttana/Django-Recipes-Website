from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms import LoginForm, RecipeForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination


@method_decorator(login_required(login_url='authors:login',
                                 redirect_field_name='next'),
                  name='dispatch')
class DashboardRecipe(View):

    def get_recipes(self, id):
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
        return render(self.request, 'authors/views/dashboard_recipe_form.html', {
            'form': form,
            'form_id': 'form_recipe_edit',

        })

    def get(self, request, id):

        recipe = self.get_recipes(id)

        form = RecipeForm(instance=recipe)

        return self.renderView(form)

    def post(self, request, id):

        recipe = self.get_recipes(id)

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
                                    args=(id,)))

        return self.renderView(form)
