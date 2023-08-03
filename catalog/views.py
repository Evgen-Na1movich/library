from django.shortcuts import render


# Create your views here.

def index_view(request):
    context = {
        'header': 'Hi, everybody who is opened this page.'
    }
    return render(request, 'index.html', context)
