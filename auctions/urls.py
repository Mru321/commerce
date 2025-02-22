from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_listings/", views.create_listings, name="create_listings"),
    path("categories/", views.categories, name="categories"),
    path("add/<int:listing_id>/", views.add, name="add"),
    path("remove/<int:listing_id>/", views.remove, name="remove"),
    path("<int:listing_id>/", views.current_listing, name="current_listing"),
    path("watchlist/", views.display_watchlist, name="display_watchlist"),
    path("comment<int:id>/", views.comment, name="comment"),
    path("add_bid/<int:listing_id>", views.add_bid, name="add_bid"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction")
    
    
]
