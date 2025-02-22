from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Auction_listings(models.Model):
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=300)
    img_url=models.CharField(max_length=3000)
    is_active=models.BooleanField()
    category=models.CharField(max_length=30)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    price=models.FloatField()
    watchlist=models.ManyToManyField(User, blank=True, null=True, related_name="listing_of_watchlist")

    def __str__(self):
        return f"Name: {self.name}, Price: {self.price}"
    


class Comment(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.CharField(max_length=300)
    listing=models.ForeignKey(Auction_listings, on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.owner.username} | Listing: {self.listing}"
    


class Bid(models.Model):
    owner=models.ForeignKey(User, on_delete=models.CASCADE)
    bid_value=models.FloatField(default=0)
    listing=models.OneToOneField(Auction_listings, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"Name: {self.owner.username} | Bid: {self.bid_value}"