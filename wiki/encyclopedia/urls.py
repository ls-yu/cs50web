from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search/", views.search, name="search"),
    path("newpage", views.new_page, name="new_page"),
    path("add", views.add, name="add")
]
