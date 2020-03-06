"""it_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from capturer import views
from django.urls import include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url 


urlpatterns = [
    path('', views.index, name = 'index'),
    path('admin/', admin.site.urls),
    path('capturer/', include('capturer.urls')),
    path('accounts/', include('registration.backends.simple.urls')),
    path(r'', include('social_django.urls', namespace='social')),
    url(r'^search/', include('haystack.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
