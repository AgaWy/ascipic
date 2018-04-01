from django.shortcuts import render

# Create your views here.

from django.views import View

from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, ImageForm
from .models import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


from img2txt import load_and_resize_image, dither_image_to_web_palette, generate_grayscale_for_image
from django.views.generic.edit import DeleteView

import PIL






# CONVERT PICTURE TO ASCII
def convertImageFromimgnameToASCII(imgname):
    maxLen = 160   # default maxlen: 100px
    bgcolor = None
    target_aspect_ratio = 0.5   # default target_aspect_ratio: 1.0
    antialias = PIL.Image.ANTIALIAS

    try:
        img = load_and_resize_image(imgname, antialias, maxLen, target_aspect_ratio)
    except IOError:
        exit("File not found: " + imgname)

    img = dither_image_to_web_palette(img, bgcolor)

    # get pixels
    pixel = img.load()

    width, height = img.size

    # string = generate_HTML_for_image(pixel, width, height)
    string = generate_grayscale_for_image(pixel, width, height, bgcolor)

    return string









# FIRST ATTEMPT TO CHECK IF IMG TO ASCII WORKS
# class StringView(View):
#
#     def get(self, request):
#         imgname = '/Users/Agnieszka/test_pic/pony.png'
#         ascii = convertImageFromimgnameToASCII(imgname)
#
#         ctx = {
#             'ascii': ascii,
#         }
#         return render(request, 'ascii.html', ctx)
# url(r'^ascii/', StringView.as_view(), name='ascii'),
# from ascipic2.views import StringView




# BASE LANDING PAGE
class ZzzView(View):
    def get(self, request):
        return render(request, 'base.html')
# url(r'^base/', ZzzView.as_view(), name='base'),
# from ascipic2.views import ZzzView





# LOGIN PAGE
class LoginView(View):

    def get(self, request):
        context = {
            'form' : LoginForm()
        }
        return render(request, 'login.html', context)


    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('/')           # PRZEJDZ DO STRONY PO ZALOGOWANIU
            else:
                error = 'bledny uzytkownik lub haslo'
        else:
            user = ""
            error = "Invalid form"

        context = {
            "form": form,
            "username": user,
            "error": error
        }
        return render(request, 'login.html', context)

# W VIEWS.PY NA GORZE DODAJ:
# from .forms import LoginForm
# from django.contrib.auth import authenticate, login, logout
# W URLS.PY DODAJ:
# from .views import LoginView
# url(r'^login/', LoginView.as_view(), name='login'),






# LOGOUT PAGE
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
# from .views import LogoutView
# url(r'^logout/', LogoutView.as_view(), name='logout'),






# SIGNUP PAGE
class SignupView(View):

    def get(self, request):
        context = {
            'form' : SignupForm()
        }
        return render(request, 'signup.html', context)


    def post(self, request):
        form = SignupForm(request.POST)
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']

        user_exists = False
        try:
            User.objects.get(username=username)
            user_exists = True
            print('uzytkownik juz istnieje')
        except ObjectDoesNotExist:
            pass

        if user_exists:
            # username = User.objects.get(username="username")
            error = 'uzytkownik juz istnieje'
            return error

        else:
            if password1 == password2:
                user = User.objects.create_user(username=username, password=password1)
            else:
                error = 'haslo nie jest jednakowe'
                return error

        return redirect('/login')

# W VIEWS.PY NA GORZE DODAJ:
# from .forms import SignupForm
# W URLS.PY DODAJ:
# from .views import SignupView
# url(r'^signup/', SignupView.as_view(), name='signup'),








# UPLOAD PHOTO PAGE
class UploadView(View):
    def get(self, request):
        form = ImageForm()
        return render(request, 'upload.html', {
            'form': form
            })

    def post(self, request):
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.save(commit=False)
            # TAKES IMAGE FROM FORM AND PRETENDS TO SAVE IT IN DATABASE

            img.ascii = convertImageFromimgnameToASCII(img.path)
            # TAKES IMAGE AND CONVERTS TO ASCII USING IMAGE PATH
            # return redirect('upload')

            try:
                img.creator = request.user
                # IT SAYS THAT CREATOR IS THE LOGGED USER
                img.save()
                # SAVING IMAGE OBJECT AS COMPLETE MODEL TO DATABASE

            except ValueError:
                pass

            ctx = {
                "name": img.name,
                "path": img.path,
                "ascii": img.ascii,
            }
            return render(request, 'show.html', ctx)

        return render(request, 'upload.html', {
            'form': form
            })
# from .views import UploadView
# url(r'^upload/', UploadView.as_view(), name='upload'),








# GALLERY PAGE
class GalleryView(View):
    def get(self, request):
        images = Image.objects.filter(creator=request.user)
        ctx = {
            'images': images
        }
        return render(request, 'gallery.html', ctx)
# from .views import GalleryView
# url(r'^gallery/', GalleryView.as_view(), name='gallery'),








# DELETE OPTION
# from django.views.generic.edit import DeleteView
class DeleteImg(DeleteView):
    model = Image
    success_url = '../gallery'
    # ASK MENTOR

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
# url(r'^delete/(?P<pk>(\d)+)', DeleteImg.as_view(), name='delete'),








