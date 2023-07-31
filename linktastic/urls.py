from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name='home'),
    path("your-links/", views.your_links, name='your-links'),
    path("url-shortener/", views.url_shortener, name='url-shortener'),
    path("settings/", views.settings, name='settings'),
    path("customize-links/", views.customize_links, name='customize-links'),
    path("customize-profile/", views.customize_profile, name='customize-profile'),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('delete_link/<int:link_id>', views.delete_link, name='delete-link'),
    path('u/<str:username>', views.public_profile, name='public-profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='linktastic/change_password.html'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='linktastic/password_change_done.html'), name='password_change_done'),
    path('<str:slug>', views.redirect_view, name='redirect')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)