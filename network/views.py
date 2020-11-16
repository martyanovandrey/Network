import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  
from django.db.models import Q

from .models import User, Post, UserFollowing

from django.views.generic import ListView

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

#This function get request and username and return Page object with username's posts divided by pages 
def post_paginator(request, username):
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user)
    #elif isinstance(username, list):

    else:
        posts = Post.objects.all()
    posts = posts.order_by("-timestamp")
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)    
    return posts


def posts(request, postbox):
    posts = post_paginator(request, postbox)
    return render(request, 'network/index.html', { 'posts': posts })



def create_post(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_post = data["post"]
        user = data["username"]
        user = User.objects.get(username=user)
        post = Post(user = user, text = new_post)
        post.save()
        return HttpResponse(status=204)
    elif request.method == "PUT":
        data = json.loads(request.body)
        print(data)
        new_post = data["post"]
        user = data["username"]
        id = data["id"]
        user = User.objects.get(username=user)
        post = Post.objects.filter(id = id).update(text = new_post)
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "POST/PUT request required."}, status=400)


@login_required(login_url='login')
def profile(request, profile):
    user = User.objects.get(id=request.user.id)
    follow = User.objects.get(username=profile)
    
    try:
        is_followed = False
        if request.method == "POST":
            UserFollowing.objects.get(user_id=user, following_user_id=follow).delete()
    except:
        UserFollowing.objects.create(user_id=user, following_user_id=follow)
        is_followed = True
    
    following = follow.following.count()
    followers = follow.followers.count()


    posts = post_paginator(request, profile)
    return render(request, 'network/profile.html', {
        'name': profile,
        'following': following,
        'followers': followers,
        'is_followed': is_followed,
        'posts': posts        
        })

def follow(request):
    user = User.objects.get(id=request.user.id)
    follow = User.objects.get(username=user)
    following = follow.following.count()
    follow_query = UserFollowing.objects.filter(user_id=user)
    follow_list = list()
    for follow in follow_query:
        follow_list.append(follow.following_user_id)
    my_filter_qs = Q()
    for user in follow_list:
        my_filter_qs = my_filter_qs | Q(user=user)
    posts = Post.objects.filter(my_filter_qs)
    posts = post_paginator(request, profile)

    #List of following users for follow_view
    follow_users = []
    for users in follow_query:
        follow_users.append(users.following_user_id.username)
    print(tuple(follow_users))

    return render(request, 'network/follow.html', {
        'name': user,
        'following': following,
        'follow_users': tuple(follow_users),
        'posts': posts})

def user_api(request):
    user = User.objects.get(id=request.user.id)
    user_following = UserFollowing.objects.filter(user_id=user)
    return JsonResponse([user_follow.serialize() for user_follow in user_following], safe=False)

