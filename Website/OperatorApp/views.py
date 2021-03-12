from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success
from django.views import View
from django.core.serializers import serialize
from django.contrib import messages

from .forms import LoginForm, OperatorForm, RegisterForm
from OperatorApp.models import Operator, Mode
from .Hypercat import hypercat

'''
Checks the data that comes inside params: /api/<params>
checks the pk value sent and returns specified operator
also checks for invalid/no pk values and returns entire list 
'''


class OperatorView(View):

    # OperatorAPI GET /operator view - returns registered operators in PAS212:2016
    # compliant format
    def get(self, request):
        params = list(request.GET.items())
        operators_list = Operator.objects.all()
        if params and (params[0][0] == 'filterString'):
            if params[0][1] == "all":
                pass
            else:
                operators_list = Operator.objects.filter(pk=params[0][1])
        serialized_operators = sorted(serialize('python', operators_list), key=lambda x: x['pk']    )
        hc = hypercat.createOperatorHypercat(serialized_operators, Mode.objects.all())
        return JsonResponse(hc, safe=False)


class ModeView(View):

    # Returns list of correctly formatted modes
    def clean_modes(self, modes):
        cleaned_modes = []
        for mode in modes:
            cleaned_modes.append({'id': mode['pk'], 'short_desc': mode['fields']['short_desc'],
                                  'long_desc': mode['fields']['long_desc']})

        return cleaned_modes

    # OperatorAPI GET /mode view - returns available modes of transport
    def get(self, request):
        params = list(request.GET.items())
        modes_list = Mode.objects.all()
        if params and (params[0][0] == 'filterString'):
            modes_list = Mode.objects.filter(pk=params[0][1])
        serialized_operators = serialize('python', modes_list)
        data = self.clean_modes(serialized_operators)
        return JsonResponse(data, safe=False)


# Register view
def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()

            # Create new operator object
            newop_name = user_form.cleaned_data['operator_name']
            newop_homepage = user_form.cleaned_data['homepage']
            newop_api_url = user_form.cleaned_data['api_url']
            newop_miptaurl = user_form.cleaned_data['miptaurl']
            newop_modes = user_form.cleaned_data['modes']
            newop_phone = user_form.cleaned_data['phone']
            newop_email = user_form.cleaned_data['email']
            newop = Operator.objects.create(admin=User.objects.get(username=user.username), name=newop_name, homepage=newop_homepage, api_url=newop_api_url, miptaurl=newop_miptaurl, phone=newop_phone, email=newop_email)
            newop.modes.set(newop_modes)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            success(request, f"Congratulations, {user.username}! You've registered successfully!")
            return redirect(reverse('operator:operators'))
        else:
            print(user_form.errors)
    else:
        user_form = RegisterForm()

    context = {
        'registration_form': user_form,
    }
    return render(request, 'OperatorApp/register.html', context)


# Login view
def operator_login(request):
    # If the user is logged in, redirect to the operators page
    if request.user.is_authenticated:
        return redirect(reverse('operator:operators'))

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Validate and clean form
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect(reverse('operator:edit'))

    return render(request, 'OperatorApp/login.html', {"form": form})


# Logout - redirect to login page
def operator_logout(request):
    logout(request)
    return redirect(reverse('operator:login'))


# Edit operator profile
def edit_profile(request):
    # If the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('operator:login')

    operator = Operator.objects.get(admin=request.user)
    form = OperatorForm(instance=operator)
    if request.method == 'POST':
        form = OperatorForm(request.POST, instance=operator)
        # Validate form
        if form.is_valid():
            form.save()
            messages.success(request, "Operator updated successfully.")
            return redirect(reverse('operator:edit'))

    return render(request, 'OperatorApp/edit-operator.html', {'form': form})


# Display all operators in a table (after an operator logs in)
def operators(request):
    # If the user is not logged in, redirect to the login page
    if not request.user.is_authenticated:
        return redirect('operator:login')

    operator_info = Operator.objects.order_by('pk')
    context_dict = {'operators': operator_info}

    return render(request, 'OperatorApp/operators.html', context_dict)
