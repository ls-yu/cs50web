from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.utils.safestring import mark_safe
import random as rand

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
            "title": title,
            "entry": util.get_entry(title)
        })

def search(request):
    form = request.GET
    search = form['q'].lower()
    print(search)
    print(util.list_entries())
    if search in (title.lower() for title in util.list_entries()):
        return entry(request, search)
    else:
        return search_results(request, search)

def search_results(request, search):
    get_items = []
    for entry in util.list_entries():
        if search in entry.lower():
            get_items.append(entry)
    return render(request, "encyclopedia/search_results.html", {
        "entries": get_items
    })

class NewPageForm(forms.Form):
    title = forms.CharField(label=mark_safe("Title"))
    content = forms.CharField(widget=forms.Textarea, label=mark_safe("Content"))

def new_page(request, title=None):
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm(),
        "title": title
    })

def add(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for page in util.list_entries():
                if page.lower() == title.lower():
                    return new_page(request, title)
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return HttpResponse("Error")

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label=mark_safe("Content"))

def edit_page(request, title):
    return render(request, "encyclopedia/edit_page.html", {
        "form": EditPageForm({'content': util.get_entry(title)}),
        "title": title
    })

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return HttpResponse("Error")
    
def random(request):
    title = util.list_entries()[rand.randint(0, len(util.list_entries()))]
    return entry(request, title)
