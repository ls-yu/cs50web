from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
#from auth.models import UserProfile
from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Watchlist


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
            watchlist=Watchlist(user=user)
            watchlist.save()
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
        exclude = ['current_bid', 'num_bids', 'state', 'seller', 'winner']
    """
    def clean(self):
        cleaned_data = super(ListingForm, self).clean()
        print(cleaned_data)
        
        if self.starting_bid <= 0:
            raise forms.ValidationError("Set a higher starting bid!")
        return cleaned_data
    
    def __init__(self, seller, *args, **kwargs):
         super(ListingForm, self).__init__(*args, **kwargs)
         self.state = True
         self.seller = seller
    """
@login_required
def new_listing(request):
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            """
            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = request.POST["starting_bid"]
            image = request.POST["image"]
            category = request.POST["category"]
            seller = request.user
            #print(seller)
            #print(starting_bid)
            listing = Listing(form.clean())

            print(listing.title, listing.description, listing.starting_bid, listing.image, listing.category)
            listing.state = True
            listing.current_bid = listing.starting_bid
            listing.num_bids = 0
            listing.seller = seller
            """
            
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            current_bid = form.cleaned_data["starting_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            seller = request.user
            listing = Listing(title=title, description=description, starting_bid=starting_bid, current_bid=starting_bid, num_bids=0, state=True, image=image, seller=seller)
            listing.save()
            print(listing)
            #print(listing.seller)
            #print(listing.starting_bid)
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
            print(form.non_field_errors)
            return HttpResponse("Error submitting form")
    else:
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {'form': form})

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        exclude = ['bidder', 'listing']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['commenter', 'listing']

def listing(request, id_number):
    listing = Listing.objects.get(pk=id_number)
    listing_comments = Comment.objects.filter(listing=listing)
    if request.method == "POST":
        if request.POST['action'] == 'Bid':
            form = BidForm(request.POST)
            if form.is_valid():
                bidder = request.user
                #this_listing = listing
                amount = form.cleaned_data["amount"]
                bid = Bid(bidder=bidder, listing=listing, amount=amount)
                if bid.amount <= listing.current_bid:
                    return HttpResponse("Bid must be higher than current bid.")
                else:
                    bid.save()
                    listing.current_bid = bid.amount
                    listing.winner = request.user
                    listing.num_bids = listing.num_bids + 1
                    listing.save()
            else:
                return HttpResponse("Error submitting bid")
        elif request.POST['action'] == 'End Auction':
            listing.state = False
            listing.save()
        elif request.POST['action'] == 'Comment':
            comment = CommentForm(request.POST)
            if comment.is_valid():
                commenter = request.user
                text = comment.cleaned_data["text"]
                new_comment = Comment(commenter=commenter, text=text, listing=listing)
                new_comment.save()
                form = BidForm()
                watching = False
            else:
                return HttpResponse("Error submitting comment")
        elif request.POST['action'] == 'Add to Watchlist':
            watchlist = get_object_or_404(Watchlist, pk=request.user)
            watchlist.listings.add(listing)
            watchlist.save()
        elif request.POST['action'] == 'Remove from Watchlist':
            watchlist = get_object_or_404(Watchlist, pk=request.user)
            watchlist.listings.remove(listing)
            watchlist.save()
        form = BidForm()
        comment = CommentForm()
        watching = False
        if request.user.is_authenticated:
            watchlist = get_object_or_404(Watchlist, pk=request.user)
            print(watchlist)
            if listing in watchlist.listings.all():
                watching = True
        return render(request, "auctions/listing.html", {'watching': watching,'listing': listing, 'form': form, 'comment': comment, 'listing_comments': listing_comments})
    else:
        form = BidForm()
        comment = CommentForm()
        watching = False
        if request.user.is_authenticated:
            watchlist = get_object_or_404(Watchlist, pk=request.user)
            print(watchlist.listings.all())
            if listing in watchlist.listings.all():
                print("watching")
                watching = True
        return render(request, "auctions/listing.html", {'watching': watching,'listing': listing, 'form': form, 'comment': comment, 'listing_comments': listing_comments})

@login_required
def watchlist(request):
    watchlist = get_object_or_404(Watchlist, pk=request.user)
    listings = watchlist.listings.all()
    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })

def category_select(request):
    return render(request, "auctions/category_select.html")

def category(request, category):
    listings = Listing.objects.filter(category=category)
    print(listings)
    return render(request, "auctions/category.html", {
        'listings':listings
    })