from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, OperatorForm
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
    operator = Operator.objects.get(admin=request.user)
    form = OperatorForm(instance=operator)

    if request.method == 'POST':
        form = OperatorForm(request.POST, instance=operator)

        if form.is_valid():
            form.save()
            messages.success(request, "Operator updated successfully.")
            return redirect(reverse('operator:edit'))

    return render(request, 'OperatorApp/edit-operator.html', {'form': form})


# display all operators (after an operator logs in)
@login_required
def operators(request):
    operator_info = Operator.objects.order_by('name')
    context_dict = {'operators': operator_info}

    return render(request, 'OperatorApp/operators.html', context_dict)
