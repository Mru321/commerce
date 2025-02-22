from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .models import Auction_listings, Comment, Bid

from .models import User


def index(request):
    if request.method=='POST':
        return HttpResponseRedirect(reverse('categories'))

    else:
        auctions_listings=Auction_listings.objects.all()
    
        return render(request, "auctions/index.html", {
            "auction_listings": auctions_listings
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listings(request):
    if request.method=='POST':
        name=request.POST['name']
        description=request.POST['description']
        img_url=request.POST['img_url']
        price=request.POST['price']
        category=request.POST['category']
        owner=request.user
        listing=Auction_listings(
            name=name, 
            description=description, 
            img_url=img_url, 
            is_active=True, 
            category=category,  
            owner=owner, 
            price=float(price))
        listing.save()

        return render(request, "auctions/create_listings.html",{
            "message":"Listing created successfully!! "
        })

    else:
        return render(request, "auctions/create_listings.html")
    


def categories(request):
    if request.method=='POST':
        category=request.POST['category']
        auctions_listings=Auction_listings.objects.filter(category=category, is_active=True)
    
        return render(request, "auctions/categories.html", {
            "category":category,
            "auction_listings": auctions_listings
        }) 

    else:
        return render(request, "auctions/index.html")   



def current_listing(request, listing_id):

    listing=Auction_listings.objects.get(pk=listing_id)
    user=request.user
    watchlist=user in listing.watchlist.all()
    comments=Comment.objects.filter(listing=listing)
    is_owner=listing.owner.username==user.username
    
    bids=Bid.objects.filter(listing=listing)
    if bids:
        bid=bids.first()
        user_is_winner=user.username==bid.owner.username
    else: 
        bid=bids
        user_is_winner=False
    
    

    return render(request, "auctions/current_listing.html", {
        "user":user,
        "watchlist":watchlist,
        "listing":listing,
        "comments":comments,
        "bid":bid,
        "is_owner":is_owner,
        "user_is_winner":user_is_winner
    })


def add(request, listing_id):
    listings=Auction_listings.objects.get(pk=listing_id)
    user=request.user
    listings.watchlist.add(user)
    return HttpResponseRedirect(reverse('current_listing', kwargs={'listing_id':listing_id}))


def remove(request, listing_id):
    listings=Auction_listings.objects.get(pk=listing_id)
    user=request.user
    listings.watchlist.remove(user)
    return HttpResponseRedirect(reverse('current_listing', kwargs={'listing_id':listing_id}))

def display_watchlist(request):
    user=request.user
    listings_in_watchlist=user.listing_of_watchlist.all()
    return render(request, "auctions/display_watchlist.html",{
        "listings_in_watchlist":listings_in_watchlist
    })
    

def comment(request, id):
    if request.method=='POST':
        comment=request.POST['comment']
        user=request.user
        listing=Auction_listings.objects.get(id=id)
        comment_1=Comment(owner=user, comment=comment, listing=listing)
        comment_1.save()

        return HttpResponseRedirect(reverse('current_listing', kwargs={'listing_id':id}))  
    else:
        return HttpResponseRedirect(reverse('current_listing', kwargs={'listing_id':id}))  
    



def add_bid(request, listing_id):
    user=request.user
    listing=Auction_listings.objects.get(id=listing_id)
    watchlist=user in listing.watchlist.all()
    comments=Comment.objects.filter(listing=listing)
    is_owner=listing.owner.username==user.username

    if request.method=='POST':
        bid_value=request.POST['bid_value']
        bid_already_exist=Bid.objects.filter(listing=listing)
        if bid_already_exist:
            bid=bid_already_exist.first()
            if float(bid_value) > bid.bid_value:
                bid.bid_value=bid_value
                bid.save()
                return render(request, "auctions/current_listing.html",{
                    "user":user,
                    "updated":True,
                    "bid":bid,
                    "watchlist":watchlist,
                    "listing":listing,
                    "comments":comments,
                    "is_owner":is_owner
                })
            else:
                return render(request, "auctions/current_listing.html",{
                    "user":user,
                    "updated":False,
                    "bid":bid,
                    "watchlist":watchlist,
                    "listing":listing,
                    "comments":comments,
                    "is_owner":is_owner
                })
                
        else:
            if float(bid_value) >= listing.price:
                bid=Bid(owner=user, bid_value=bid_value, listing=listing)
                bid.save()
                return render(request, "auctions/current_listing.html",{
                        "user":user,
                        "updated":True,
                        "bid":bid,
                        "watchlist":watchlist,
                        "listing":listing,
                        "comments":comments,
                        "is_owner":is_owner
                    })
            else:
                return render(request, "auctions/current_listing.html",{
                        "user":user,
                        "updated":False,
                        "watchlist":watchlist,
                        "listing":listing,
                        "comments":comments,
                        "is_owner":is_owner
                    })  

    else:
        return HttpResponseRedirect(reverse('current_listing', kwargs={'listing_id':listing_id})) 


def close_auction(request, listing_id):
    listing=Auction_listings.objects.get(id=listing_id)
    listing.is_active=False
    listing.save()

    user=request.user
    watchlist=user in listing.watchlist.all()
    comments=Comment.objects.filter(listing=listing)
    is_owner=listing.owner.username==user.username

    bids=Bid.objects.filter(listing=listing)
    if bids:
        bid=bids.first()
        user_is_winner=user.username==bid.owner.username
    else: 
        bid=bids
        user_is_winner=False

    
    return render(request, "auctions/current_listing.html",{
                    "user":user,
                    "updated":True,
                    "bid":bid,
                    "watchlist":watchlist,
                    "listing":listing,
                    "comments":comments,
                    "is_owner":is_owner,
                    "message":"Your auction is closed Successfully!! ",
                    "user_is_winner":user_is_winner
                })

