from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ get all data of user, needed for login """
    pass

class categoryModel(models.Model):
    """ get the name of the category """
    name = models.CharField(max_length = 50)
    
    """ this function return the name of the category, in the admin panel """
    def __str__(self):
        return self.name
    
    
class bid(models.Model):
    """ this model is for get all data from each object that the user created """
    bid = models.DecimalField(
        max_digits = 9, 
        decimal_places = 2
        )
    ownerName = models.ForeignKey(
        User,
        on_delete = models.CASCADE, 
        related_name = "BidOwner"
        )
    
    def __str__(self):
        return f"{self.bid} by {self.ownerName} "    


class listing(models.Model):
    """ this model is for get all data from each object that the user created """
    title = models.CharField(max_length = 50)
    description = models.TextField()
    url = models.CharField(max_length = 300)
    price = models.ForeignKey(bid, on_delete=models.CASCADE, related_name="Bid")
    status =  models.BooleanField(default = True)
    ownerName = models.ForeignKey(
        User,
        on_delete = models.CASCADE, 
        related_name = "Owner"
        )
    category = models.ForeignKey(
        categoryModel, 
        on_delete=models.CASCADE, 
        related_name="Category"
        )
    watched = models.ManyToManyField(User, related_name="WatchList", blank = False)
    
    """ this function return the title of the item, in the admin panel """
    def __str__(self):
        return self.title
    
    
class comment(models.Model):
    """ this model is for get all data from each object that the user created """
    comment = models.TextField()
    ownerName = models.ForeignKey(
        User,
        on_delete = models.CASCADE, 
        related_name = "CommentOwner"
        )
    listing = models.ForeignKey(
        listing, 
        on_delete=models.CASCADE, 
        related_name="Comment"
        )
    
    def __str__(self):
        return f"{self.ownerName} said: {self.comment}"
    
