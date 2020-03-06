from django import forms
from capturer.models import Photo, UserProfile, Tag, Review, Contact
from django.contrib.auth.models import User

class PhotoForm(forms.ModelForm):
    Image = forms.ImageField(help_text="Please upload the image.", required=False) 
    Title = forms.CharField(max_length=Photo.TITLE_MAX_LENGTH,
                            help_text="Please input the title.")
    Description = forms.CharField(max_length=Photo.DESCRIPTION_MAX_LENGTH,
                                  help_text="Please description your art.")
    Like = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    Tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple())
    # Category = forms.CharField(widget=forms.HiddenInput(), max_length=30)

    class Meta:
        model = Photo
        exclude = ('Category', 'author', 'Date')

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
    # content = forms.CharField(max_length=1000 ,widget=forms.Textarea)
    class Meta:
        model = Review
        fields = ('content', )


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('question', )