from django.contrib import messages
from django.shortcuts import Http404, redirect, render

from authors.forms import RegisterForm

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'authors/views/register.html', {
        'form': form,
    })


def create_view(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(
            request, "Your user is created successfully, please log in.")

        del (request.session['register_form_data'])

    return redirect('authors:register')
