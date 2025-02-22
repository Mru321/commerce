from django.contrib import admin
from .models import User, Auction_listings, Comment, Bid
# Register your models here.
admin.site.register(User)
admin.site.register(Auction_listings)
admin.site.register(Comment)
admin.site.register(Bid)