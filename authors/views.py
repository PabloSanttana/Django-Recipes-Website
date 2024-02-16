from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import Http404, redirect, render
from django.urls import reverse

from authors.forms import LoginForm, RecipeForm, RegisterForm
from recipes.models import Recipe
from utils.pagination import make_pagination

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/views/register.html', {
        'form': form,
        'form_action': reverse('authors:create'),
        'form_id': 'register_user',
    })


def create_view(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(
            request, "Your user is created successfully, please log in.")

        del (request.session['register_form_data'])

        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('authors:dashboard')

    form = LoginForm()
    return render(request, 'authors/views/login.html', {
        'form': form,
        'form_action': reverse('authors:login_create'),
        'form_id': 'login_user'
    })


def login_create(request):

    if not request.POST:
        raise Http404()

    POST = request.POST
    form = LoginForm(POST)

    if form.is_valid():

        authenticated_user = authenticate(
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password')
        )

        if authenticated_user is not None:
            messages.success(
                request, "Your are logged in.")
            login(request, authenticated_user)

            return redirect('authors:dashboard')

        else:
            messages.error(request, 'Invalid credentials')

    else:
        messages.error(request, 'Invalid username or password.')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):

    if not request.POST:
        return redirect('authors:login')

    if request.POST.get('username') != request.user.username:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, 10)
    # Contar o número total de receitas não publicadas
    total_recipes = recipes.count()

    return render(request, 'authors/views/dashboard.html', {
        'recipes': page_obj,
        'total_recipes': total_recipes,
        'pagination_range': pagination_range
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_register(request):
    register_recipe_form_data = request.session.get(
        'register_recipe_form_data', None)

    form = RecipeForm(register_recipe_form_data)

    return render(request, 'authors/views/dashboard_recipe_form.html', {
        'form': form,
        'form_action': reverse('authors:dashboard_recipe_create'),
        'form_id': 'register_recipe',

    })


def dashboard_recipe_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_recipe_form_data'] = POST

    form = RecipeForm(
        POST,
        files=request.FILES or None,
    )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()
        messages.success(request, 'Recipe created sucess')

        del (request.session['register_recipe_form_data'])

        return redirect('authors:dashboard')

    return redirect('authors:dashboard_recipe_register')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=id
    ).first()
    if not recipe:
        raise Http404()

    form = RecipeForm(data=request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.save()

        messages.success(request, 'Recipe edited successfully')

        return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

    return render(request, 'authors/views/dashboard_recipe_form.html', {
        'form': form,
        'form_id': 'register_edit',

    })
