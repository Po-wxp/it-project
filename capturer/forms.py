from django import forms
from capturer.models import Photo, UserProfile, Tag, Review, Contact, Category
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from datetime import datetime


class PhotoForm(forms.ModelForm):   

    Image = forms.ImageField(required=False)
    Title = forms.CharField(max_length=Photo.TITLE_MAX_LENGTH)
    Description = forms.CharField(max_length=Photo.DESCRIPTION_MAX_LENGTH)
    Tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple(),required=False)
    # Category = forms.CharField(widget=forms.HiddenInput(), max_length=30)

    class Meta:
        model = Photo
        exclude = ('author', 'Date','Like','views','Tag','Category')
        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', )
        

class UserProfileForm(forms.ModelForm):
    image = forms.ImageField(help_text="Please upload the image.", required=False) 
    nickname = forms.CharField(max_length=UserProfile.NICKNAME_MAX_LENGTH, help_text="Please input your nickname")
    CHOICES=[('male','male'), ('female','female')]
    gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    description = forms.CharField(max_length=UserProfile.DESCRIPTION_MAX_LENGTH, help_text="Please input the description")
    postcode = forms.CharField(max_length=UserProfile.POSTCODE_MAX_LENGTH, help_text="Please input the postcode")

    class Meta:
        model = UserProfile
        fields = ('image', 'nickname', 'gender', 'description', 'postcode', )

class UserProfileModifyForm(forms.ModelForm):
    image = forms.ImageField(help_text="Please upload the image.", required=False) 
    nickname = forms.CharField(max_length=UserProfile.NICKNAME_MAX_LENGTH, help_text="Please input your nickname")
    description = forms.CharField(max_length=UserProfile.DESCRIPTION_MAX_LENGTH, help_text="Please input the description")
    postcode = forms.CharField(max_length=UserProfile.POSTCODE_MAX_LENGTH, help_text="Please input the postcode")

    class Meta:
        model = UserProfile
        fields = ('image', 'nickname', 'description', 'postcode', )


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('content', )
    # def clean(self):
    #     # content = self.cleaned_data['content']
    #     try:
    #         model_class = ContentType.objects.get(model=content).model_class()
    #     except ObjectDoesNotExist:
    #         raise forms.ValidationError('review is not exist!')
    #     return self.cleaned_data


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('question', )