from django.shortcuts import render
from django.http import HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    
    if util.get_entry(title) is None:
        return HttpResponse(f"Error: Could not find a page for {title.capitalize()}!")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "entry": util.get_entry(title)
        })
