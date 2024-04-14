from django.shortcuts import render
 
def login(request):
    context = {}
    context['hello'] = 'Hello, Fuck World and ALL!'
    return render(request, 'login.html', context)