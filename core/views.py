from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import Profile, Post, LikePost, FollowersCount, Contact
from .forms import ContactForm

from itertools import chain
import random

# Create your views here.
@login_required(login_url='signin')
def index(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    
    feed_list = list(chain(*feed))

    # Recomendacion de usuarios para agregar
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if x not in list(user_following_all)]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in current_user)]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)
    
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
    
    suggestions_username_profile_list = list(chain(*username_profile_list))

    return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "El correo electronico ya existe")
                return redirect('signup')
            elif User.objects.filter(username=username):
                messages.info(request, "El nombre de usuario ya existe")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()


                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # creamos el objeto perfil para el nuevo usuario
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, "Las contraseñas no coinciden")
            return redirect('signup')
    
    else:
        return render(request, "signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        
        # Este if evalua que si el usuario no esta en la base de datos devuelve un None.
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Datos incorrectos")
            return redirect('signin')

    else:
        return render(request, "signin.html")

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):

    user_profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        
        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            print(request.FILES.get('image'))
            image = request.FILES.get('image')
            first_name = request.POST['first-name']
            last_name = request.POST['last-name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def profile(request, pk):

    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        buton_text = "Dejar de seguir"
    else:
        buton_text = "Seguir"
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        "user_object": user_object,
        "user_profile": user_profile,
        "user_posts": user_posts,
        "user_posts_length": user_posts_length,
        "buton_text": buton_text,
        "user_followers": user_followers,
        "user_following": user_following,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def upload(request):
    
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get("image-upload")
        caption = request.POST["caption"]

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect("/")

    else:
        return redirect("/")

@login_required(login_url='signin')
def like_post(request):
    
    username = request.user.username
    post_id = request.GET.get("post_id")

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.likes += 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.likes -= 1
        post.save()
        return redirect('/')

@login_required(login_url='signin')
def follow(request):
    
    if request.method == "POST":
        
        follower = request.POST["follower"]
        user = request.POST["user"]
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect("/profile/" + user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect("/profile/" + user)
    else:
        return redirect("/")

@login_required(login_url='signin')
def search(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)

        username_profile_list = list(chain(*username_profile_list))

    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def contact(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == "POST":
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            messages.success(request, "Muchas gracias por tu contacto")
            
            info = contact_form.cleaned_data

            contact = Contact(name=info['name'], surname=info['surname'], message=info['message'], email=info['email'])

            contact.save()


    else:
        contact_form = ContactForm()

    return render(request, "contact.html", {'contact_form': contact_form, 'user_profile': user_profile})

def terms(request):
    return render(request, "terms.html")

def policy(request):
    return render(request, "policy.html")

def about(request):
    return render(request, "about.html")


