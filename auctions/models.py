from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime 



class User(AbstractUser):
    pass

class Category (models.Model) :
    name = models.CharField (max_length= 50)
    
    def __str__(self) :
        return self.name

        
class Item (models.Model) :
    title = models.CharField (max_length= 100)
    description = models.TextField ()
    price = models.DecimalField (max_digits=8, decimal_places=2)
    picture = models.URLField (blank= True, null= True)
    user = models.ForeignKey (User, on_delete=models.CASCADE, related_name= 'user')
    active =models.BooleanField (default= True)
    category = models.ForeignKey (Category, on_delete= models.CASCADE, blank= True, null= True, related_name= 'category')
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f"{self.title, self.user}"

  
class Watchlist (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "watchlist_user")
    item_post= models.ManyToManyField (Item, blank= True, related_name= "item_watchlist")
    
    
class Comment (models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_comment")
    item_commented = models.ForeignKey(Item, on_delete=models.CASCADE, blank= True, null= True, related_name= "item_commented")    
    comment = models.TextField(blank=False)
    date_creation = models.DateTimeField (auto_now_add=True, null= True)
    
    def __str__(self) :
        return f"{self.user} commented : {self.comment}"
    
class Bid (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    item_bid = models.ForeignKey(Item, on_delete=models.CASCADE, blank= True, null=True, related_name="item_bid" )
    value = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return f"{self.user} bid:{self.value} for {self.item_bid}"