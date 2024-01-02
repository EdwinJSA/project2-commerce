from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import createListingForm, searchByCatedory
from .models import User, listing, categoryModel,comment, bid


def index(request):
    itemsActivated = listing.objects.filter(status = True)
    # print(itemsActivated.get(id = 4).url)
    return render(request, "auctions/index.html",{
        "items": itemsActivated,
        "form": searchByCatedory()
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


# my functions #

def newlisting(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["url"]
        price = request.POST["price"]
        status = request.POST["status"]
        nameCategory = categoryModel.objects.get(id = int(request.POST["category"]))
        ownerName = request.user
        
        print(title, description, url, price, status, nameCategory, ownerName)
        
        Bid = bid(bid=int(price), ownerName=ownerName)
        Bid.save()
        
        newElement = listing(
            title = title,
            description = description,
            url = url,
            price = Bid,
            status = status,
            category = nameCategory,
            ownerName = ownerName
        )
        
        newElement.save()
        return HttpResponseRedirect(reverse("index"))
    
    
    return render(request, "auctions/newlisting.html",{
        'form': createListingForm()
    })
    
def displayCategory(request):
    print(request.POST["category"])
    elements = listing.objects.filter(category = categoryModel.objects.get(id = int(request.POST["category"])))
    return render (request, "auctions/index.html",{
        "items": elements,
        "form": searchByCatedory()
    })
    
def listingitem(request, id):
    item = listing.objects.get(id = id)
    allow = request.user == item.ownerName
    return render(request, "auctions/listingitem.html",{
        "item": item,
        "listingWatched": False,
        "allowed": allow
    })
    
def removeWatchlist(request, id):
    removelisting = listing.objects.get(id = id)
    comments = comment.objects.filter(listing = id)
    
    # print("--------------------------------------")    
    # print("eliminando a: ", request.user)
    
    removelisting.watched.remove(request.user)
    
    # print("---LISTA FINAL REMOVIDA----")
    # for i in removelisting.watched.all():
    #     print(i)
    # print("--------------------------------------")
        
    return render(request, "auctions/listingitem.html",
                  {"listingWatched": False,
                   "item" : listing.objects.get(id = id),
                   "comments": comments})

def addToWatchlist(request, id):    
    addlisting = listing.objects.get(id = id)
    comments = comment.objects.filter(listing = addlisting)
    
    # print("--------------------------------------")    
    # print("Aagregando a: ", request.user)
    
    addlisting.watched.add(request.user)
    
    # print("---LISTA FINAL Agregada----")
    # for i in addlisting.watched.all():
    #     print(i)
    # print("--------------------------------------")
    
    return render(request, "auctions/listingitem.html",
                  {"listingWatched": True,
                   "item" : listing.objects.get(id = id),
                   "comments": comments})

def watchlist(request):
    userWatchlist = listing.objects.filter(watched = request.user)
    currentUser = request.user
    
    
    
    # print("--------------------------------------")
    # for i in userWatchlist:
    #     if i.price.ownerName == currentUser:
    #         print(f"{i.title} es del propietario {currentUser}")
    # print("--------------------------------------")
    
    return render(request, "auctions/watchlist.html",{
        "listUserWatchlist": userWatchlist,
        "currentUser": currentUser
    })

def addComment(request, id):
    listingitem = listing.objects.get(id=id)
    comment_text = request.POST["newComment"]

    newComment = comment(
        comment=comment_text,
        ownerName=request.user,
        listing=listingitem
    )    
    newComment.save()
    
    comments = comment.objects.filter(listing = listingitem)

    return render(request, "auctions/listingitem.html", {
        "item": listingitem,
        "comments": comments
    })
    
def addBid(request, id):
    comments = comment.objects.filter(listing = id)
    listingitem = listing.objects.get(id=id)
    newBid = request.POST["newBid"]
    
    if listingitem.status == True:
        if int(listingitem.price.bid) < int(newBid):
            listingitem.price.bid = newBid
            listingitem.price.ownerName = request.user
            listingitem.price.save()
            return render(request, "auctions/listingitem.html", {
            "item": listingitem,
            "message": "Your bid has been added.",
            "comments": comments
            })
        
        return render(request, "auctions/listingitem.html", {
            "item": listingitem,
            "message": "Your bid must be higher than the current price."
        })  
        
    return render(request, "auctions/listingitem.html", {
        "item": listingitem,
        "message": "Your listing is closed."
    })
    
def closeListing(request, id):
    listingitem = listing.objects.get(id=id)
    listingitem.status = False
    listingitem.save()
    return render(request, "auctions/listingitem.html", {
        "item": listingitem
    })
    
