from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import LoginForm
from OperatorApp.models import Operator

# login operator
def operator_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect(reverse('operator:operators'))

    return render(request, 'OperatorApp/login.html', {"form": form})

# log out operator
@login_required
def operator_logout(request):
    logout(request)
    return redirect(reverse('operator:login'))

# edit operator profile
@login_required
def edit_profile(request):
    user = request.user
    try:
        operator_info = Operator.objects.get(admin=user)
    except:
        operator_info = None

    context_dict = {'operator': operator_info}
    return render(request, 'OperatorApp/edit-operator.html', context_dict)

# display all operators (after an operator logs in)
@login_required
def operators(request):
    operator_info = Operator.objects.order_by('name')
    context_dict = {'operators': operator_info}

    return render(request, 'OperatorApp/operators.html', context_dict)
