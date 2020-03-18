from django.urls import path
from capturer import views
from django.conf.urls import url 
from django.urls import include
app_name = 'capturer'

urlpatterns = [
     path('', views.index, name='index'),
     path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
     path('post_photo/', views.post_photo, name='post_photo'),
     path('login/signup/', views.register, name='register'),
     path('login/', views.user_login, name='login'),
     path('logout/', views.user_logout, name='logout'),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
     path('<username>/profile/', views.profile, name='profile'),
     path('<username>/profile/modify/', views.ProfileModify.as_view(), name='profileModify'),
     # path('<username>/album/', views.album, name='album'),
     # path('<username>/favorite/', views.favorite, name='favorite'),
     # path('<username>/myreview/', views.myreview, name='myreview'),
     # path('<username>/following/', views.following, name='following'),
     path('category/<slug:category_name_slug>/<photo_id>/', views.show_photo, name='show_photo'),
     path('accounts/', include('registration.backends.simple.urls')),
     path('like_photo/', views.LikePhotoView.as_view(), name='like_photo'),
     path('follow/<username>/', views.follow, name='follow'),
     path('collection/<photo_id>/', views.collection, name='collection'),
     path('<photo_id>/delete/', views.delete_post, name='delete'),
     path('<photo_id>/upload_comment/', views.upload_comment, name='upload_comment'),
     path('passwordChange/', views.change_password, name='change_password'),
     # path('display_photo/', views.display_photo, name='display_photo'),

     # path('search/', views.search, name='search'),
]