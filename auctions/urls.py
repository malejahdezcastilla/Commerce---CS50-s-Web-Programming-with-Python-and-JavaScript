from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name= "create_listing"),
    path("item/<int:id>", views.item, name= "item"),
    path("close/<int:id>", views.close_auction, name= "close_auction"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name= "add_to_watchlist"),
    path("watchlist/", views.watchlist_personal, name= "watchlist"),
    path("delete_from_watchlist/<int:id>", views.delete_from_watchlist, name= "delete_from_watchlist"),
    path("categories", views.categories, name="categories"),
    path("comments/<int:id>", views.comments, name= "comments"),
    path("bid/<int:id>", views.add_bid, name= "add_bid")
]

