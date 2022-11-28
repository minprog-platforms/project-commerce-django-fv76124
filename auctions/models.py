from django.contrib.auth.models import AbstractUser
from django.db import models

# define models for application where each model represents some type of data i want to store in my databsase
# user model represents each user of the application, it inherits from abstractuser, it will have fields for username etc. 
# add models to file to represent details about auction listings, bids, comments, auction categories
class User(AbstractUser):
    pass

class Bid(models.Model):
    bid = models.IntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="userBid")

class AuctionListing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    imageurl = models.CharField(max_length=300)
    startingbid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="startingbid")
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, blank=True, null=True, related_name="user")

    def __str__(self):
        return (f"{self.title} {self.description} {self.startingbid}")
