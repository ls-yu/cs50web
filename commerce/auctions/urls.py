from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("listing/<int:id_number>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category_select", views.category_select, name="category_select"),
    path("category/<str:category>", views.category, name="category")
]
