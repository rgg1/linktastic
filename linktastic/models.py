from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=BASE62_ALPHABET):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0] * 7
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    encoded = ''.join(arr)
    while len(encoded) < 7:
        encoded = '0' + encoded
    return encoded

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    links = models.ManyToManyField(Link)
    display_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

BUTTON_SHAPES = [
    ('SQUARE', 'Square'),
    ('ROUNDED', 'Rounded'),
]

ICONS = [
    ('NONE', 'None'),
    ('STAR', 'Star'),
    ('HEART', 'Heart'),
]

FONT_SIZES = (
    ('12px', 'Small'),
    ('16px', 'Medium'),
    ('20px', 'Large'),
)

FONT_COLORS = (
    ('black', 'Black'),
    ('blue', 'Blue'),
    ('red', 'Red'),
)


class UserLinkDisplayPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    font_size = models.CharField(max_length=10, choices=FONT_SIZES, default='16px')
    font_color = models.CharField(max_length=10, choices=FONT_COLORS, default='black')
    font = models.CharField(max_length=100, default='default_font')
    button_shape = models.CharField(max_length=10, choices=BUTTON_SHAPES, default='SQUARE')
    icon = models.CharField(max_length=10, choices=ICONS, default='NONE')

    class Meta:
        verbose_name_plural = "User link display preferences"

class ShortenedURL(models.Model):
    id = models.AutoField(primary_key=True)  
    original_url = models.URLField()
    slug = models.CharField(max_length=20, null=True)

    def generate_slug(self):  
        return base62_encode(self.id)  