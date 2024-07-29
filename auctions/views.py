from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Item, Category, Watchlist, Comment, Bid


def index(request):
    active_items = Item.objects.filter (active=True)
     
    return render(request, "auctions/index.html", {
        "items": active_items
    })


def item (request, id):
    listing_item = Item.objects.get(pk=id)
    owner = request.user.username == listing_item.user.username
    all_coments = Comment.objects.filter(item_commented = listing_item).order_by("-date_creation")
    success_message = request.GET.get('success_message')
    error_message = request.GET.get('error_message')
    highest_bid = Bid.objects.filter(item_bid = listing_item).order_by("-value").first()

    
    try:
        highest_bid_user = highest_bid.user
    except AttributeError:
        return render (request, "auctions/item.html", {
        "item": listing_item,
        "owner": owner,
        "comments": all_coments,
        "success_message" : success_message,
        "error_message": error_message,

    })
    
    return render (request, "auctions/item.html", {
        "item": listing_item,
        "owner": owner,
        "comments": all_coments,
        "success_message" : success_message,
        "error_message": error_message,
        "highest_bid_user": highest_bid_user,
    })



def create_listing (request) :
    if request.method == "GET":
        list_categories = Category.objects.all().order_by("name")
        return render (request, "auctions/create_listing.html", {
            "categories":list_categories
        })
        
    else :
     title= request.POST ["title"]
     description= request.POST ["description"]
     price= request.POST ["price"] 
     url_image= request.POST ["url_image"]
     category= request.POST ["category"]  
     user = request.user
     date = Item.creation_date
     category_name = Category.objects.get(name=category)
     
     new_listing = Item(
         title= title,
         description= description,
         price= float(price),
         picture= url_image,
         user= user,
         category= category_name,
         creation_date= date         
     )
     new_listing.save()
     
     return redirect ("index")


def close_auction (request,id) :
    item = Item.objects.get (pk=id)
    owner = request.user.username == item.user.username
    if request.user.username == item.user.username :
        item = Item.objects.get (pk=id)
        item.active  = False
        item.save ()
        
        return render (request, "auctions/item.html", {
            "item": item,
            "success_message": "Congratulations! Closed auction.",
            "owner": owner
    })
        
    else :    
        return render (request, "auctions/item.html", {
            "item": item,
            "error_message": "You can't close this auction",
            "owner": owner
    })
        
        
def add_to_watchlist (request, id):
    item_to_add= Item.objects.get (pk=id)
    if Watchlist.objects.filter(user= request.user, item_post=item_to_add).exists():
        return render (request, "auctions/item.html", {
            "item": item_to_add,
            "error_message": "You already have this item in your watchlist !"
    })
    
    watchlist_user, created= Watchlist.objects.get_or_create (user=request.user)
    watchlist_user.item_post.add(item_to_add)
    return render (request, "auctions/item.html", {
            "item": item_to_add,
            "success_message": "Succesfully added to your watchlist !",
            "watchlist_user": watchlist_user
    })

    
def watchlist_personal (request):
    current_user = request.user
    
    try:
        watchlist= Watchlist.objects.get(user = current_user)
    except Watchlist.DoesNotExist:
        return render (request, "auctions/watchlist.html", {
                "message":"Add items to see your watchlist",
                })
    
    else:
        return render (request, "auctions/watchlist.html", {
                "watchlist": watchlist,
                })

    
def delete_from_watchlist (request, id):
    item_to_delete = Item.objects.get(pk=id)
    print(id, item_to_delete)
    watchlist = Watchlist.objects.get(user= request.user)
    if request.method == "POST" :
        watchlist.item_post.remove(item_to_delete)
        return render (request, "auctions/watchlist.html", {
             "watchlist": watchlist,
             "message": "Item removed from Watchlist!"
        })

def categories (request):
    if request.method == "POST":
        all_categories = Category.objects.all().order_by("name")
        selected_category = request.POST["category"]
        get_category = Category.objects.get (name=selected_category)
        active_items = Item.objects.filter (active=True, category=get_category)
        if not active_items :
            return render (request, "auctions/categories.html", {
                    "message": "No items found for this category"
                })
    
        return render (request, "auctions/categories.html", {
            "categories": all_categories,
            "active_items": active_items,
        })


    selected_category = request.GET.get("category")
    if selected_category == None :
        all_categories = Category.objects.all().order_by("name")
        
        return render (request, "auctions/categories.html", {
                "categories": all_categories
        })       


def comments (request, id) :
    if request.method == "POST": 
        comment= request.POST ["comment"]
        user = request.user
        item = Item.objects.get(pk=id)
        
        new_comment = Comment (
            user = user,
            item_commented = item,
            comment = comment   
        )

        new_comment.save ()
        
    return redirect ("item", id= item.id)

def add_bid (request, id):
    new_bid = float (request.POST ["new_bid"])
    item = Item.objects.get(pk=id)
    user = request.user
    highest_bid = Bid.objects.filter(item_bid = item).order_by("-value").first()
    query = QueryDict(mutable=True)
    
    if item.user == user:
        query["error_message"] = "Seller can not bid"
     
        view_item_url = reverse("item", args=[item.id])
        query_string = query.urlencode()
        redirect_url = '{}?{}'.format(view_item_url, query_string)
            
        return redirect (redirect_url)    
        
    
    if highest_bid != None:
        minimun_price = highest_bid.value
    else:
        minimun_price = item.price
        
        
    if new_bid > minimun_price :
        
        add_bid = Bid (
            user= user,
            item_bid= item,
            value= new_bid       
        )
        add_bid.save()
        query["success_message"] = "Bid added succesfully"
    
    else:
        query["error_message"] = f"Bid must be greater than {minimun_price}"
                
        
    view_item_url = reverse("item", args=[item.id])
    query_string = query.urlencode()
    redirect_url = '{}?{}'.format(view_item_url, query_string)
        
    return redirect (redirect_url)


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
