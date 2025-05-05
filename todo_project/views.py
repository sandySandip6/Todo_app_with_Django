from django.http import HttpResponse

def homepage(request):
    return HttpResponse("welcome to the todo app")

