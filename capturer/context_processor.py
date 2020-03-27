from capturer.models import Category, Photo , UserProfile, Review, Tag
from capturer.forms import PhotoForm
def nav_bar(request):
    context_dict = {
        'post_photo_form' : PhotoForm(),
        'categories': Category.objects.all(), 
        'tags': Tag.objects.all(),
        'authors' : UserProfile.objects.all(), 
    }
    return(context_dict)
