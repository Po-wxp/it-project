from django.shortcuts import render, redirect
from capturer.models import Category, Photo , UserProfile, Review, Tag
from capturer.forms import PhotoForm, UserForm, UserProfileForm, UserProfileModifyForm, ReviewForm, ContactForm
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from capturer.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from itertools import chain
from django.contrib import messages
import haystack.views

# helper method
def stable(request):
    try:
        user = request.user
        current_user_profile = UserProfile.objects.get_or_create(user=user)[0]
    except:
        user=None
        current_user_profile=None
    return current_user_profile

def base_query():
    context_dict = {
        
    }
    return context_dict

def index(request):
    context_dict = {}

    most_popular_sub = Photo.objects.order_by('-views')[:3]
    most_popular=Photo.objects.order_by('-Like')[:1]
    all_photos = Photo.objects.order_by('-Like')

    top_photos = set()
    categories = Category.objects.all()
    for c in categories:
        photo = Photo.objects.filter(Category = c).order_by('-Like')[:1]
        for p in photo:
            top_photos.add(p)

    # print(top_photos)
    
    context_dict = {'top_cat_photos':top_photos, 'most_popular_sub' : most_popular_sub,
                    'most_popular': most_popular, 'all_photos': all_photos,
                    'profile':stable(request),
                    }
    context_dict.update(base_query())
    return render(request, 'capturer/index.html', context=context_dict)

def about(request):
    context_dict = {}
    current_user_profile = stable(request)
    context_dict['profile'] = current_user_profile
    context_dict.update(base_query())
    return render(request, 'capturer/about.html', context=context_dict)

@login_required
def contact(request):
    context_dict = {}
    context_dict['profile'] = stable(request)

    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.question = request.POST.get('question')
                form.save()
                return redirect(reverse('capturer:index'))
        else:
            print(form.errors)
    context_dict['form'] = form
    context_dict.update(base_query())
    return render(request, 'capturer/contact.html', context=context_dict)

@login_required
def show_category(request, category_name_slug):
    context_dict = {}
    context_dict['profile'] = stable(request)
    context_dict.update(base_query())
    try:
        category = Category.objects.get(slug=category_name_slug)
        
        most_popular=Photo.objects.filter(Category=category).order_by('-Like')[:1]
  
        #The filter() will return a list of page objects or an empty list
        photos = Photo.objects.filter(Category=category).order_by('-Like')[1:]
        
        #Add results list to the template context under name pages
        context_dict['photos'] = photos
        context_dict['category'] = category
        context_dict['most_popular'] = most_popular
    except Category.DoesNotExist:
        context_dict['photos'] = None
        context_dict['category'] = None
        context_dict['most_popular'] = None
    return render(request, 'capturer/category.html', context=context_dict)
    
@login_required
def post_photo(request):
    
    user = request.user

    if request.method == 'POST':
        print(request.POST)
        print("123")
        form = PhotoForm(request.POST)
        if form.is_valid():

            photo = form.save(commit=False)
            photo.views = 0
            photo.Like = 0
            photo.Title = request.POST.get('Title')
            photo.Description = request.POST.get('Description')
            photo.author = user
            input_tags=request.POST.get('tags').split()

            photo.Category = Category.objects.get(name = request.POST.get('Category'))
            if 'Image' in request.FILES:
                photo.Image = request.FILES['Image']
        
            photo.save()
            for input_tag in input_tags:
                if Tag.objects.filter(name = input_tag).exists(): 
                    photo.Tag.add(Tag.objects.get(name = input_tag))
                else:
                    Tag.objects.create(name = input_tag)
                    photo.Tag.add(Tag.objects.get(name = input_tag))
            # print(tags)
            return redirect(reverse('capturer:index'))
        else:
            print(form.errors)
    return redirect(reverse('capturer:index'))               

    
def register(request):
    #if the registeration was secessful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            #save the user's form data to the database
            user = user_form.save()
    
            user.set_password(user.password)
            user.save()
            #Now sort the UserProfile instance
            #set commit=False. This delays saving the model
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.nickname = request.POST.get('nickname')
            profile.gender =  profile_form.cleaned_data.get('gender')
            profile.description = request.POST.get('description')
            profile.postcode = request.POST.get('postcode')

            if 'image' in request.FILES:
                profile.image = request.FILES['image']

            profile.save()
            registered = True
            # return redirect(reverse('capturer:index'))

        else:
            print(user_form.errors, profile_form.errors)

    else:
        #Not a HTTP POST, so we render our form using two ModelForm instance
        #These forms will be blank, reandy for user input
        user_form = UserForm()
        profile_form = UserProfileForm()
  
    context_dict = {'user_form':user_form, 'profile_form':profile_form,'registered':registered,}
    context_dict.update(base_query())
    return render(request, 'capturer/register.html', context=context_dict)

def user_login(request):
    context_dict = {}
    context_dict.update(base_query())

    if request.method == 'POST':
        username = request.POST.get('username')             
        password = request.POST.get('password') 

        #Use Dajngo's machinery to attempt to see if the username/password
        user = authenticate(username=username, password=password)

        # If we have a User Object, the details are correct
        # If none, no user
        if user:
            # Is the account active. It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect(reverse('capturer:index'))
            else:      
                # An inactive accounted was used - no logging in!
                return HttpResponse("Your account is disabled.")   
        else:
            # Bad login details were provided. So we cannot log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login from
    # This scenario would most likely be a HTTP GET.
    else:
        # No context varible to pass to the template system, hence the blank dictionary object...
        return render(request, 'capturer/login.html', context=context_dict)

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('capturer:index'))

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        album = Photo.objects.filter(author=user)
        favorite = user_profile.favorite.all()
        review = Review.objects.filter(profile = user_profile)
        review_photos = set() 
        for r in review:
            review_photos.add(r.photo)
        print(review_photos)
        followingAuthorsPhoto= set()
        for follow_author in user_profile.following.all() :
            photos = Photo.objects.filter(author = follow_author)
            for photo in photos:
                followingAuthorsPhoto.add(photo)
        follower = set()
        users = User.objects.all()
        for u in users:
            profile = u.userprofile
            followers = profile.following.all()
            if user in followers:
                follower.add(u)
            
        # print(followingAuthorsPhoto)
        # print(favorite)
        best_photo = album.order_by('-Like')[:1] 
        follower_length = len(follower)
    except user.DoesNotExist:
        user = None
    
    if user is None:
        return redirect('/capturer/')
    
    context_dict = {'selected_user': user, 'album': album, 'user_profile':user_profile, 
    'favorite':favorite,
    'following':followingAuthorsPhoto,
    'follower_length':follower_length,
    'review_photos':review_photos,
    'profile':stable(request), 'best_photo':best_photo,}
    context_dict.update(base_query())
    return render(request, 'capturer/profile.html', context=context_dict)

class ProfileModify(View): 
    def get_user_details(self, username): 
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        form = UserProfileModifyForm({'nickname': user_profile.nickname,
                                      'description': user_profile.description, 
                                      'postcode': user_profile.postcode,
                                      'image': user_profile.image})
        return (user, user_profile, form)

    @method_decorator(login_required) 
    def get(self, request, username): 
        try: 
            (user, user_profile, form) = self.get_user_details(username) 
        except TypeError: 
            return redirect(reverse('capturer:index'))
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form,
                         'profile':stable(request)}
        return render(request, 'capturer/profileModify.html', context_dict)

    @method_decorator(login_required) 
    def post(self, request, username): 
        try: 
            (user, user_profile, form) = self.get_user_details(username) 
        except TypeError: 
            return redirect(reverse('capturer:index'))
        form = UserProfileModifyForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid(): 
            form.save(commit=True) 
            return redirect('capturer:profile', user.username) 
        else: 
            print(form.errors)
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form, 'categories': Category.objects.all()}
        return render(request, 'capturer/profileModify.html', context_dict)

@login_required
def show_photo(request,category_name_slug, photo_id):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category


    except Category.DoesNotExist:
        context_dict['category'] = None
    try:
        photo = Photo.objects.get(id=photo_id)
        author_profile = UserProfile.objects.get(user = photo.author)
        tags = photo.Tag.all()
        reviews = Review.objects.filter(photo=photo).order_by('-id')
        context_dict = {'photo':photo,'photo_tags':tags, 'reviews':reviews, 'author_profile':author_profile}
    except Photo.DoesNotExist:
        context_dict['photo'] = None
        context_dict['photo_tags'] = None
        context_dict['reviews'] = None
    related_photos = Photo.objects.filter(Category=category).exclude(id=photo_id)

    context_dict['form_review'] = ReviewForm()
    context_dict['profile'] = stable(request)
    context_dict['related_photos'] =related_photos
    context_dict.update(base_query())
    
    # visit cookie
    response = render(request, 'capturer/show_photo.html', context=context_dict)
    visits = int(request.COOKIES.get('visits_'+photo_id, photo.views))
    last_visite  = request.COOKIES.get('last_visit_'+photo_id, str(datetime.now()))
    last_visit_time = datetime.strptime(last_visite[:-7],'%Y-%m-%d %H:%M:%S')
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits +1
        photo.views = visits
        photo.save()
        response.set_cookie('last_visit_'+photo_id, str(datetime.now()))
    else:
        response.set_cookie('last_visit_'+photo_id, last_visite)
    response.set_cookie('visits_'+photo_id, visits)    
    return response
     

@login_required
def upload_comment(request, photo_id):
    form = ReviewForm(request.POST)
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    photo = Photo.objects.get(id=photo_id)

    data = {}
    if form.is_valid():
        comment = Review()
        comment.photo = photo            
        comment.profile = user_profile
        comment.like = 0
        comment.content = request.POST.get('content')
        comment.save()
        # return redirect(reverse('capturer:show_category', kwargs={'category_name_slug':category_name_slug}))
        data['status'] = "success"
        data['content'] = comment.content
        data['date'] = comment.date.strftime('%Y-%m-%d %H:%I:%S')
        data['profile_name'] = comment.profile.user.username
        data['profile_avatar'] = comment.profile.image.url
    else:
        data['status'] = "error"
        data['message'] = list(form.errors.values())[0][0]
    return JsonResponse(data)

class LikePhotoView(View): 

    @method_decorator(login_required) 
    def get(self, request): 
        photo_id = request.GET['photo_id']
        try:
            photo = Photo.objects.get(id=int(photo_id)) 
        except Photo.DoesNotExist: 
            return HttpResponse(-1) 
        except ValueError: 
            return HttpResponse(-1)
        photo.Like = photo.Like + 1 
        photo.save()
        return HttpResponse(photo.Like)


@login_required
def collection(request, photo_id): 
    use_profile = stable(request)
    photo = Photo.objects.get(id=int(photo_id)) 
    
    data = {}
    if use_profile.favorite.filter(id = photo.id).exists():
        use_profile.favorite.remove(photo)
        data['message'] = "2"
    else:
        use_profile.favorite.add(photo)
        data['message'] = "1"
    return JsonResponse(data, safe=False)


@login_required
def follow(request, username):
    current_user_profile = stable(request)
    selected_user = User.objects.get(username = username)

    data = {}
    if current_user_profile.following.filter(username=selected_user.username).exists():
        current_user_profile.following.remove(selected_user)
        data['message'] = "2"
        # "You canceled following {}".format(selected_user)
    else:
        current_user_profile.following.add(selected_user)
        data['message'] = "1"
        # "You are now following {}".format(selected_user)
    return JsonResponse(data, safe=False)

@login_required
def delete_post(request, photo_id):
    user = request.user
    photo = Photo.objects.get(id=int(photo_id))

    if photo.author == user:
        photo.delete()
    
    return redirect(reverse('capturer:profile', kwargs={'username':user.username}))


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('capturer:index')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'capturer/passwordChange.html', {'form': form, 'categories': Category.objects.all()})

def tag_photo(request, tag_name):
    context_dict = {}
    photos = set()
    try:
        tag = Tag.objects.get(name = tag_name)
        all_photo = Photo.objects.all()
        for photo in all_photo:
            tags = photo.Tag.all()
            for t in tags:
                if t == tag:
                    photos.add(photo)
        # print(photos)
        context_dict['photos'] = photos
    except tag.DoesNotExist:
        context_dict['photos'] = None
    context_dict.update(base_query())
    return render(request,'capturer/tag_photo.html', context = context_dict)

class SearchView(haystack.views.SearchView):
    categories = Category.objects.all(),
    
    def extra_context(self):
        return {
            'categories': categories,
        }