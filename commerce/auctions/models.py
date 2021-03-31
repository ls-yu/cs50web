from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal

class User(AbstractUser):
    pass


class Listing(models.Model):
    BOOKS = 'BOOKS'
    CLOTHING = 'CLOTHING'
    COLLECTIBLES = 'COLLECTIBLES'
    ELECTRONICS = 'ELECTRONICS'
    CRAFTS = 'CRAFTS'
    TOYS = 'TOYS'
    HOME = 'HOME'
    PET = 'PETS'
    SPORTS = 'SPORTS'

    CATEGORY_CHOICES = [
        (BOOKS, 'Books'),
        (CLOTHING, 'Clothing'),
        (COLLECTIBLES, 'Collectibles'),
        (CRAFTS, 'Crafts'),
        (TOYS, 'Toys'),
        (HOME, 'Home'), 
        (PET, 'Pet'), 
        (SPORTS, 'Sports')
    ]
    category = models.CharField(
        max_length=12,
        choices=CATEGORY_CHOICES,
        default=BOOKS
    )
    auto_increment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    seller = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="listings")
    description = models.CharField(max_length=1000)
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(blank=True)
    current_bid = models.DecimalField(max_digits=6, decimal_places=2) # will have to set this to the max value of the bids
    num_bids = models.IntegerField()
    state = models.BooleanField()
    winner = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, related_name="auctions_won")
    
    def __str__(self):
        return f"{self.title}: sold by {self.seller}. (starting bid: {self.starting_bid}, current bid: {self.current_bid}.)"

class Bid(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    bidder = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(to=Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bidder} offering ${self.amount} on {self.listing.title}"


class Comment(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    text = models.TextField(max_length=500)
    listing = models.ForeignKey(to=Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.commenter} comments: {self.text} on {self.listing}"

class Watchlist(models.Model):
    user = models.OneToOneField(to=User, primary_key=True, on_delete=models.CASCADE, related_name="user")
    listings = models.ManyToManyField(Listing, blank=True, related_name="listings")

    def __str__(self):
        return f"{self.user} is watching {self.listings}"

