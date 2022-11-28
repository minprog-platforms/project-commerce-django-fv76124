from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bid

def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all()
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
    
def activelisting(request, id):
    listingdata = AuctionListing.objects.get(pk=id)
    isOwner = request.user.username == listingdata.owner.username
    return render(request, "auctions/activelisting.html", {
        "listing": listingdata,
        "isOwner": isOwner,
    })

def addlisting(request):
    if request.method == "GET":
        return render(request, "auctions/addlisting.html")
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        startingbid = request.POST["startingbid"]
        currentuser = request.user
        
        bid = Bid(bid=int(startingbid), user=currentuser)
        bid.save()
        
        NewListing = AuctionListing(
            title=title,
            description=description,
            imageurl=imageurl,
            startingbid=bid,
            owner=currentuser    
        )
        NewListing.save()
        
        return HttpResponseRedirect(reverse("index"))
            
def bid(request, id):
    addbid = request.POST["bid"]
    listingdata = AuctionListing.objects.get(pk=id)
    if int(addbid) > listingdata.startingbid.bid:
        newbid = Bid(user=request.user, bid=int(addbid))
        newbid.save()
        listingdata.startingbid = newbid
        listingdata.save()
        return render(request, "auctions/activelisting.html", {
            "listing": listingdata
        })
    else:
        return render(request, "auctions/error.html", {
            "error": "Your bid is too low"
            })

def closedlisting(request, id):
    listingdata = AuctionListing.objects.get(pk=id)
    listingdata.isActive = False
    listingdata.save()
    isOwner = request.user.username == listingdata.owner.username
    return render(request, "auctions/activelisting.html", {
        "listing": listingdata,
        "isOwner": isOwner,
    })
        
        
        
    
    
    

