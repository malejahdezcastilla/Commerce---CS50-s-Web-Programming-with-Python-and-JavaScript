from django.contrib import admin
from .models import Item, Category, User, Watchlist, Comment, Bid

# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Watchlist)
admin.site.register(Comment)
admin.site.register(Bid)
