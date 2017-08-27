from django.shortcuts import render
from django.shortcuts import HttpResponse


from .models import Post

# Create your views here.

def post_list(request) :
    queryset = Post.objects.all()
    context = {
        "title": "Post Lists",
        "post_list": queryset
    }
    #return HttpResponse("<h1>Welcome</h1>")
    return render(request, "post_list.html", context)