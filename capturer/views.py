from django.shortcuts import render
from capturer.models import Category, Photo , UserProfile, Review
from capturer.forms import PhotoForm, UserForm, UserProfileForm, UserProfileModifyForm, ReviewForm, ContactForm
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from capturer.bing_search import run_query
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
# Create your views here.
def stable(request):
    try:
        user = request.user
        current_user_profile = UserProfile.objects.get_or_create(user=user)[0]
    except:
        user=None
        current_user_profile=None
    return current_user_profile

def index(request):
    context_dict = {}
    
    category_list = Category.objects.all()
    # photo_list = Photo.objects.order_by('-Like')[:5]

    category1_photo_list = Photo.objects.filter(Category = Category.objects.get(id=1)).order_by('-Like')[:1]
    category2_photo_list = Photo.objects.filter(Category = Category.objects.get(id=2)).order_by('-Like')[:1]
    category3_photo_list = Photo.objects.filter(Category = Category.objects.get(id=3)).order_by('-Like')[:1]
    category4_photo_list = Photo.objects.filter(Category = Category.objects.get(id=4)).order_by('-Like')[:1]
    category5_photo_list = Photo.objects.filter(Category = Category.objects.get(id=5)).order_by('-Like')[:1]
    category6_photo_list = Photo.objects.filter(Category = Category.objects.get(id=6)).order_by('-Like')[:1]
    category7_photo_list = Photo.objects.filter(Category = Category.objects.get(id=7)).order_by('-Like')[:1]
    category8_photo_list = Photo.objects.filter(Category = Category.objects.get(id=8)).order_by('-Like')[:1]

    context_dict = {'category1': category1_photo_list, 'category2': category2_photo_list,
                    'category3': category3_photo_list, 'category4': category4_photo_list,
                    'category5': category5_photo_list, 'category6': category6_photo_list,
                    'category7': category7_photo_list, 'category8': category8_photo_list,
                    'categories':category_list, 'profile':stable(request)}

    # context_dict = {'categories':category_list, 'profile':stable(request)}

    return render(request, 'capturer/index.html', context=context_dict)

def about(request):
    context_dict = {}
    current_user_profile = stable(request)
    context_dict['profile'] = current_user_profile
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
    return render(request, 'capturer/contact.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    context_dict['profile'] = stable(request)
    try:
        category = Category.objects.get(slug=category_name_slug)
        #The filter() will return a list of page objects or an empty list
        photos = Photo.objects.filter(Category=category)
        
        #Add results list to the template context under name pages
        context_dict['photos'] = photos
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['photos'] = None
        context_dict['category'] = None

    return render(request, 'capturer/category.html', context=context_dict)
    
@login_required
def post_photo(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/capturer/')

    form = PhotoForm()

    user = request.user

    if request.method == 'POST':
        form = PhotoForm(request.POST)

        if form.is_valid():
            if category:
                photo = form.save(commit=False)
                photo.Category = category
                photo.views = 0
                photo.Like = 0
                photo.Title = request.POST.get('Title')
                photo.Description = request.POST.get('Description')
                photo.author = user
                photo.tag=request.user
                
                if 'Image' in request.FILES:
                    photo.Image = request.FILES['Image']
            
                photo.save()
                form.save_m2m()

                return redirect(reverse('capturer:show_category', kwargs={'category_name_slug':category_name_slug}))
        else:
            print(form.errors)
                
    context_dict = {'form' : form, 'category': category, 'profile':stable(request)}
    return render(request, 'capturer/post_photo.html', context=context_dict) 

    
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
  
    context_dict = {'user_form':user_form, 'profile_form':profile_form,'registered':registered}
    return render(request, 'capturer/register.html', context=context_dict)


# def upload_avatar(request):
#     file_obj = request.FILES.get('image')
#     file_path = os.path.join('static/image/', file_obj.name)
#     with open(file_path, 'wb') as f:
#         for chunk in file_obj.chunks():
#             f.write(chunk)
#     return HttpResponse(file_path)



def user_login(request):
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
        return render(request, 'capturer/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('capturer:index'))


# A helper method 
def get_server_side_cookie(request, cookie, default_val=None): 
    val = request.session.get(cookie) 
    if not val: 
        val = default_val 
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    # Get the number of visits to this site
    # COOKIES.get() function is to obtain the visits cookie
    # If the cookie exists, the value returned is casted to an integer
    # If the cookie doesn't exist, then the default value of 1 is used
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it is been more than a day since the last visit..
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    
    # Update/set the visits cookie
    request.session['visits'] = visits   

def profile_base(username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        album = Photo.objects.filter(author=user)
    except user.DoesNotExist:
        user = None
    
    if user is None:
        return redirect('/capturer/')

    return (user,user_profile, album)

@login_required
def profile(request, username):
    (user, user_profile, album) = profile_base(username)
    context_dict = {'selected_user': user, 'user_profile':user_profile, 'album':album, 'profile':stable(request)}
    return render(request, 'capturer/profile.html', context=context_dict) 

@login_required
def album(request, username):
    (user, user_profile, album) = profile_base(username)
    context_dict = {'selected_user': user, 'album': album, 'user_profile':user_profile, 'profile':stable(request)}
    return render(request, 'capturer/album.html', context=context_dict) 

@login_required
def favorite(request, username):
    (user, user_profile, album) = profile_base(username)
    photos = user_profile.favorite.all()
    
    context_dict = {'selected_user': user,'photos':photos,'user_profile':user_profile,'album':album, 'profile':stable(request)}
    return render(request, 'capturer/favorite.html', context=context_dict) 

@login_required
def myreview(request, username):
    (user, user_profile, album) = profile_base(username)
    reviews = Review.objects.filter(profile = user_profile)
    context_dict = {'selected_user': user,'reviews':reviews,'user_profile':user_profile,'album':album,'profile':stable(request)}
    return render(request, 'capturer/myreview.html', context=context_dict) 

@login_required
def following(request, username):
    (user, user_profile, album) = profile_base(username)
    followings = user_profile.following.all()
    context_dict = {'selected_user': user,'followings':followings, 'user_profile':user_profile,'album':album,'profile':stable(request)}
    return render(request, 'capturer/following.html', context=context_dict)



# def search(request):
#     result_list = []

#     if request.method == 'POST':
#         query = request.POST['query'].strip()
#         if query:
#             result_list = run_query(query)

#     return render(request, 'capturer/search.html',{'result_list': result_list})


class ProfileModify(View): 
    def get_user_details(self, username): 
        (user, user_profile, album) = profile_base(username)
        form = UserProfileModifyForm({'nickname': user_profile.nickname,
                                      'description': user_profile.description, 
                                      'postcode': user_profile.postcode,
                                      'image': user_profile.image})
        return (user, user_profile, form, album)

    @method_decorator(login_required) 
    def get(self, request, username): 
        try: 
            (user, user_profile, form, album) = self.get_user_details(username) 
        except TypeError: 
            return redirect(reverse('capturer:index'))
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form,
                        'album':album, 'profile':stable(request)}
        return render(request, 'capturer/profileModify.html', context_dict)

    @method_decorator(login_required) 
    def post(self, request, username): 
        try: 
            (user, user_profile, form, album) = self.get_user_details(username) 
        except TypeError: 
            return redirect(reverse('capturer:index'))
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid(): 
            form.save(commit=True) 
            return redirect('capturer:profile', user.username) 
        else: 
            print(form.errors)
        context_dict = {'user_profile': user_profile, 'selected_user': user, 'form': form,'album':'album'}
        return render(request, 'capturer/profileModify.html', context_dict)

@login_required
def show_photo(request, category_name_slug, photo_id):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
    try:
        photo = Photo.objects.get(id=photo_id)
        tags = photo.Tag.all()
        reviews = Review.objects.filter(photo=photo).order_by('-id')
        context_dict = {'photo':photo,'tags':tags, 'reviews':reviews}
    except Photo.DoesNotExist:
        context_dict['photo'] = None
        context_dict['tags'] = None
        context_dict['reviews'] = None

    # form = ReviewForm()
    # user = request.user
    # user_profile = UserProfile.objects.get(user=user)

    # if request.method == 'POST':
    #     form = ReviewForm(request.POST)
    #     if form.is_valid():
    #         if category:
    #             if photo:
    #                 form = form.save(commit=False)
    #                 form.photo = photo            
    #                 form.profile = user_profile
    #                 form.like = 0
    #                 form.content = request.POST.get('content')
    #                 form.save()
    #                 # return redirect(reverse('capturer:show_category', kwargs={'category_name_slug':category_name_slug}))
    #     else:
    #         print(form.errors)
    # 
    context_dict['form'] = ReviewForm()
    context_dict['profile'] = stable(request)

    visitor_cookie_handler(request)
    photo.views = request.session['visits']
    photo.save()
    response = render(request, 'capturer/show_photo.html', context=context_dict)
    return response

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

def delete_post(request, photo_id):
    user = request.user
    photo = Photo.objects.get(id=int(photo_id))

    if photo.author == user:
        photo.delete()
    
    return redirect(reverse('capturer:profile', kwargs={'username':user.username}))
   
 
    