from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'OperatorApp/index.html')

# login operator
def login(request): 
    pass

# log out operator
def logout(request):
    pass

# display operator profile
def profile(request):
    pass

# edit operator profile
def edit_profile(request):
    pass

# display all operators (when an operator logs in)
def operators(request):
    pass