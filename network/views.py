from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.core.serializers import serialize
from .forms import PostForm
from django.views.decorators.csrf import csrf_exempt

import json

from .models import User, Post, Like


def index(request):
    return render(request, "network/index.html")


def all_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-timestamp')#.prefetch_related('post_likes')
        # Paginator
        paginator = Paginator(posts, 9000)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Check if the current user likes the post or not and get the like_count
        liked_post = {}
        like_count = {}
        # What does this mean?
        user_likes = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

        for post in page_obj:
            liked_post[post.id] = post.id in user_likes
            like_count[post.id] = post.post_likes.count()

        return JsonResponse({
            "posts": [post.serialize() for post in page_obj], 
            "liked_post": liked_post,
            "current_user": request.user.username,
            "like_count": like_count,
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
            }, safe=False)
    
    else:
        posts = Post.objects.all().order_by('-timestamp')
        # Paginator
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            "posts": [post.serialize() for post in page_obj],
            "has_next": page_obj.has_next(),
            "has_prev": page_obj.has_previous(),
            "total_pages": paginator.num_pages,
            "current_page": page_obj.number
            }, safe=False)


@login_required
def delete_account(request, user_id):
    if request.method == 'DELETE':
        if user_id == request.user.id:
            target_account = request.user
            target_account.delete()
            return JsonResponse({"message": "account deleted"})
        
        return JsonResponse({"message": "You cannot delete other users' accounts."}, status=403)
        
    return JsonResponse({"message": "Invalid request method"}, status=405)



@login_required
def delete_squeek(request, post_id):
    if request.method == 'DELETE':
        target_squeek = get_object_or_404(Post, id=post_id)

        # Check if it's the owner's squeek to delete
        if target_squeek.sender != request.user:
            return JsonResponse({"message": "You cannot delete other users' squeeks"}, status=403)
        
        target_squeek.delete()
        return JsonResponse({"message": "Squeek removed"}, status=200)
    
    return JsonResponse({"message": "Invalid request method"}, status=405)


@login_required(login_url='login')
def edit_post(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            post = Post.objects.get(id=post_id)
            if request.user == post.sender:
                data = json.loads(request.body)
                post.post_content = data.get('post_content', '')
                post.edited_timestamp = timezone.now()
                post.save()
                return JsonResponse({
                    "edited_timestamp": post.edited_timestamp.strftime('%d %b, %Y at %H:%M'),
                    "message": "Post edited successfully"
                }, status=200)
            else:
                return JsonResponse({"Error": "Not authorized to edit post"}, status=403)


@login_required
def following_posts(request):
    if request.user.is_authenticated:
        return render(request, 'network/following.html')
    else:
        return redirect('login')


def following_posts_data(request):
    if request.method == 'GET':
        user_following = request.user.following.all()
        # Get posts from following by 
        following_posts = Post.objects.filter(sender__in=user_following).order_by("-timestamp")

        # Get likes
        if request.user.is_authenticated:
            user_likes = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
            # Faster search in a set
            user_likes_set = set(user_likes)

        # Serialize the posts
        posts_data = [
            {
                "id": post.id,
                "sender": post.sender.username,
                "sender_id": post.sender.id,
                "post_content": post.post_content,
                "timestamp": post.timestamp,
                "edited_timestamp": post.edited_timestamp if post.edited_timestamp else "Not edited",
                "like_count": post.post_likes.count(),
                "liked": post.id in user_likes_set
            }
            for post in following_posts
        ]

        return JsonResponse({
            "posts": posts_data,
            #"following": following,
            #"following_count": following_count,
            #"followers_count": followers_count,
            "current_user": request.user.username,
            "liked_post": {post.id: post.id in user_likes for post in following_posts},
            #"like_count": like_count
        })


def follow_unfollow(request, user_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                target_user = User.objects.get(id=user_id)
            except:
                raise ValueError("User does not exist", status=404)
            
            if request.user.following.filter(id=target_user.id):
                request.user.following.remove(target_user)
                following = False
            else:
                request.user.following.add(target_user)
                following = True
            return JsonResponse({
                "following": following,
                "following_count": target_user.following.count(),
                "followers_count": target_user.followers.count(),
            }, status=200)

    return JsonResponse({'error': 'Invalid request method'})
        


@login_required
def like_unlike(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            post = Post.objects.get(id=post_id)

            with transaction.atomic():
                like, created = Like.objects.get_or_create(user=user, post=post)

            if not created:
                # The like already exists, so remove it
                like.delete()
                liked = False

            else:
                # The like was just created
                liked = True
            
            # Update the like count and return it and the like_status
            like_count = Like.objects.filter(post=post).count()

            return JsonResponse({
                "liked": liked,
                "like_count": like_count
            })
    else:
        return JsonResponse({"error": "User not authenticated"}, status=401)


#@login_required(login_url='login')
#def new_post(request):
 #   if request.user.is_authenticated:
  #      if request.method == 'POST':
   #         new_post_content = request.POST['new-post-content']
    #        sender = request.user
     #       post = Post(
      #          sender=sender,
       #         post_content=new_post_content
        #    )
         #   post.save()
        #return HttpResponseRedirect(reverse(index))


@login_required
@csrf_exempt
def new_post(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        form = PostForm(data)
        if form.is_valid():
            post = form.save(commit=False)  # Do not commit to the database yet
            post.sender = request.user      # Set the sender to the currently logged-in user
            post.save()                    # Save the post to the database
            return JsonResponse({'success': True, 'post': post.id}, status=201)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@login_required(login_url='login')
def profile(request, user_id):
    try:
        profile_person = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValueError("User does not exist")
    
    own_profile = (profile_person == request.user)
    
    return render(request, 'network/profile.html', {
        'user_id': user_id,
        'own_profile': own_profile,
        'profile_person': profile_person
    })



def profile_data(request, user_id):
    try:
        profile_person = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=404)

    user_posts = Post.objects.filter(sender=profile_person).order_by("-timestamp")

    # Is user on own profile
    own_profile = (profile_person == request.user)

    paginator = Paginator(user_posts, 9000)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Followers and following
    following = request.user.following.filter(pk=profile_person.pk).exists()
    following_count = profile_person.following.count()
    followers_count = profile_person.followers.count()

    # Check if the current user likes the post or not and get the like_count
    liked_post = {}
    like_count = {}
    if request.user.is_authenticated:
        user_likes = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

        for post in page_obj:
            liked_post[post.id] = post.id in user_likes
            like_count[post.id] = post.post_likes.count()

    # Serialize the posts
    posts_data = [
        {
            "id": post.id,
            "sender": post.sender.username,
            "post_content": post.post_content,
            "timestamp": post.timestamp,
            "edited_timestamp": post.edited_timestamp if post.edited_timestamp else "Not edited",
            "like_count": post.post_likes.count()
        }
        for post in page_obj
    ]

    return JsonResponse({
        "posts": posts_data,
        "own_profile": own_profile,
        "profile_username": profile_person.username,
        "following": following,
        "following_count": following_count,
        "followers_count": followers_count,
        "current_user": request.user.username,
        "current_user_id": request.user.id,
        "liked_post": liked_post,
        "like_count": like_count
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
