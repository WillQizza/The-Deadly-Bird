"""
URL configuration for deadlybird project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('following.urls')),
    path('api/', include('identity.urls')),
    path('api/', include('likes.urls')),
    path('api/', include('nodes.urls')),
    path('api/', include('posts.urls')),
    re_path(r'.*', include('react.urls'))   # Note: ALL API urls should be above this path so that they are searched first
]
