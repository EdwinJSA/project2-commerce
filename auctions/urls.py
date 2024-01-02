from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listingitem, name="listing"),
    path("removeWatchlist/<int:id>", views.removeWatchlist, name="removeWatchlist"),
    path("addToWatchlist/<int:id>", views.addToWatchlist, name="addToWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
]

