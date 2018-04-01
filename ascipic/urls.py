"""ascipic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin


# from ascipic2.views import StringView
from ascipic2.views import ZzzView
from ascipic2.views import LoginView, SignupView, LogoutView, UploadView, GalleryView
from ascipic2.views import DeleteImg




from django.conf import settings
from django.conf.urls.static import static


urlpatterns = ([
    url(r'^admin/', admin.site.urls),
    # url(r'^ascii/', StringView.as_view(), name='ascii'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^signup/', SignupView.as_view(), name='signup'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^upload/', UploadView.as_view(), name='upload'),
    url(r'^gallery/', GalleryView.as_view(), name='gallery'),
    url(r'^$', ZzzView.as_view(), name='base'),
    url(r'^delete/(?P<pk>(\d)+)', DeleteImg.as_view(), name='delete'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))