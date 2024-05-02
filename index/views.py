from django.shortcuts import render
 
def login(request):
    context = {}
    context['hello'] = 'Hello, Fuck World and ALL!'
    return render(request, 'login.html', context)

def tour(request):
    context = {
        "user_avatar": 'https://img1.baidu.com/it/u=4254524521,1617500748&fm=253&fmt=auto&app=138&f=JPEG?w=503&h=500'
    }
    return render(request, 'tour.html', context)