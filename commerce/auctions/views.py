from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
#from auth.models import UserProfile

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()

    return render(request, "auctions/index.html", {
        "listings": listings
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

# form for creating a new listing
class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ['current_bid', 'num_bids', 'state', 'seller']

def new_listing(request):
    form = ListingForm(request.POST)
    if request.method == "POST":
        if form.is_valid():

            title = request.POST["title"]
            #seller = UserProfile.objects.get(user=self.request.user)
            description = request.POST["description"]
            starting_bid = request.POST["starting_bid"]
            image = request.POST["image"]
            category = request.POST["category"]
            seller = request.user
            print(seller)
            print(starting_bid)
            listing = Listing(title=title, description=description, starting_bid=starting_bid, current_bid=starting_bid, num_bids=0, state=True, image=image, seller=seller)
            listing.save()
            print(listing.seller)
            print(listing.starting_bid)
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
            return HttpResponse("Error submitting form")
    else:
        return render(request, "auctions/new_listing.html", {'form': form})

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['bidder', 'listing']

def listing(request, id_number):
    listing = Listing.objects.get(pk=id_number)
    form = BidForm(request.POST)
    if request.method == "POST":
        
        if form.is_valid():
            bidder = request.user
            this_listing = listing
            amount = request.POST["amount"]
            bid = Bid(bidder=bidder, listing=this_listing, amount=amount)
            print(type(amount))
            print(type(listing.current_bid))
            if bid.amount <= listing.current_bid:
                return HttpResponse("Bid must be higher than current bid.")
            else:
                
                bid.save()
                return render(request, "auctions/listing.html", {'listing': listing, 'form': form})
        
    else:
        return render(request, "auctions/listing.html", {'listing': listing, 'form': form})