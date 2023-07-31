from django import forms
from .models import Link, UserProfile, UserLinkDisplayPreference
from django.core.exceptions import ValidationError
from urllib.parse import urlparse

class LinkForm(forms.ModelForm):
    url = forms.URLField(widget=forms.TextInput) # Override the URL field with client side validation disabled
    class Meta:
        model = Link
        fields = ['title', 'url']

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            if '://' not in url:
                # Prepend 'http://' if no scheme (http, https, ftp, etc.) is provided
                url = 'http://' + url
            parsed = urlparse(url)
            if not bool(parsed.netloc) and bool(parsed.path):
                # If the url is still invalid, raise a validation error
                raise ValidationError('Please enter a valid URL')
        return url
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'profile_picture']

class UserLinkDisplayPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserLinkDisplayPreference
        fields = ['font_size', 'font_color', 'button_shape', 'icon']

class URLShortenerForm(forms.Form):
    original_url = forms.URLField(widget=forms.TextInput)

    def clean_original_url(self):
        original_url = self.cleaned_data.get('original_url')
        if original_url:
            if '://' not in original_url:
                original_url = 'http://' + original_url
            parsed = urlparse(original_url)
            if not bool(parsed.netloc) and bool(parsed.path):
                raise forms.ValidationError('Please enter a valid URL')
        return original_url