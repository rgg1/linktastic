from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.conf import settings

from .forms import LinkForm, UserProfileForm, UserLinkDisplayPreferenceForm, URLShortenerForm
from .models import Link, UserProfile, UserLinkDisplayPreference, ShortenedURL

# Create your views here.

def login_required_message(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            messages.info(request, "You must be logged in to do that.")
            return HttpResponseRedirect(reverse(settings.LOGIN_URL))
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def home(request):
  return render(request, 'linktastic/home.html')

@login_required_message
def your_links(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            profile = UserProfile.objects.get(user=request.user)
            profile.links.add(link)
            messages.success(request, 'Link added successfully.')
            return redirect('your-links')
    else:
        form = LinkForm()

    profile = UserProfile.objects.get(user=request.user)
    links = profile.links.all()
    return render(request, 'linktastic/your-links.html', {'form': form, 'links': links})

@login_required_message
def settings(request):
  return render(request, 'linktastic/settings.html')

@login_required_message
def url_shortener(request):
  return render(request, 'linktastic/url-shortener.html')

@login_required_message
def customize_links(request):
  return render(request, 'linktastic/customize-links.html')

@login_required_message
def customize_profile(request):
  return render(request, 'linktastic/customize-profile.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = form.data.get('username').lower()  # Get the lowercased username
        form.data = form.data.copy()  # Make a copy
        form.data['username'] = username  # Replace the username with the lowercased username
        if form.is_valid():
            form.save()
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration successful.')
            default_pref = UserLinkDisplayPreference(user=user, font_color='black', font_size='Medium')
            default_pref.save()
            return redirect('your-links')
    else:
        form = UserCreationForm()
    return render(request, 'linktastic/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        username = form.data.get('username').lower()
        form.data = form.data.copy()
        form.data['username'] = username
        if form.is_valid():
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('your-links')
        else:
            pass
    else:
        form = AuthenticationForm()
    return render(request, 'linktastic/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

@login_required_message
def delete_link(request, link_id):
    link = Link.objects.get(pk=link_id)
    if request.user.userprofile.links.filter(pk=link_id).exists():
        request.user.userprofile.links.remove(link)
        messages.success(request, 'Link deleted successfully.')
        return redirect('your-links')
    else:
        messages.error(request, 'Link not found.')
        return redirect('your-links')
    
def public_profile(request, username):
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    links = user.userprofile.links.all()
    user_pref = UserLinkDisplayPreference.objects.get(user=user)
    return render(request, 'linktastic/public_profile.html', {'username': username, 'links': links, 'user_profile': user_profile, 'user_pref': user_pref})

@login_required_message
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'linktastic/edit_profile.html', {'form': form})

@login_required_message
def customize_links(request):
    try:
        user_pref = UserLinkDisplayPreference.objects.get(user=request.user)
    except UserLinkDisplayPreference.DoesNotExist:
        user_pref = UserLinkDisplayPreference(user=request.user)

    if request.method == 'POST':
        form = UserLinkDisplayPreferenceForm(request.POST, instance=user_pref)
        if form.is_valid():
            form.save()
            messages.success(request, 'Link display preferences updated successfully.')
            return redirect('settings')
    else:
        form = UserLinkDisplayPreferenceForm(instance=user_pref)

    return render(request, 'linktastic/customize-links.html', {'form': form})

@login_required_message
def url_shortener(request):
    if request.method == 'POST':
        form = URLShortenerForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            shortened = ShortenedURL(original_url=original_url)
            shortened.save()  # First save to generate an id
            shortened.slug = shortened.generate_slug()  
            shortened.save()  # Save again to store the computed slug
            short_url = request.scheme + '://' + request.get_host() + reverse('redirect', args=[shortened.slug])
            return render(request, 'linktastic/url-shortener.html', {'form': form, 'short_url': short_url})

    else:
        form = URLShortenerForm()

    return render(request, 'linktastic/url-shortener.html', {'form': form})

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_decode(string, alphabet=BASE62_ALPHABET):
    base = len(alphabet)
    strlen = len(string)
    num = 0

    for idx, char in enumerate(string):
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)

    return num

def redirect_view(request, slug):
    try:
        id = base62_decode(slug)
        obj = get_object_or_404(ShortenedURL, id=id)
    except ValueError:
        return HttpResponse('Invalid slug')
    except Http404:
        return HttpResponse(f'No ShortenedURL with id {id}')
    else:
        return redirect(obj.original_url)