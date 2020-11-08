import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from .models import User, Post, UserFollowing

def index(request):

    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def posts(request):
    posts = Post.objects.filter(user=request.user)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


def create_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    new_post = data["post"]
    user = data["username"]
    user = User.objects.get(username=user)
    post = Post(user = user, text = new_post)
    post.save()
    return HttpResponse(status=204)

def profile(request, profile):
    user = User.objects.get(id=request.user.id)
    follow = User.objects.get(username=profile)
    try:
        UserFollowing.objects.get(user_id=user, following_user_id=follow).delete()
        is_followed = False
    except:
        UserFollowing.objects.create(user_id=user, following_user_id=follow)
        is_followed = True
    
    following = user.following.count()
    followers = user.followers.count()
    return render(request, 'network/profile.html', {
        'name': profile,
        'following': following,
        'followers': followers,
        'is_followed': is_followed        
        })

def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

