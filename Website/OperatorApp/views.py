from django.shortcuts import render
from django.http import HttpResponse

# login operator
def login(request): 
    # TODO
    return render(request, 'OperatorApp/login.html')

# log out operator
def logout(request):
    # TODO
    return render(request, 'OperatorApp/login.html')

# edit operator profile
def edit_profile(request):
    # TODO
    return render(request, 'OperatorApp/edit-operator.html')

# display all operators (after an operator logs in)
def operators(request):
    # TODO
    pass
