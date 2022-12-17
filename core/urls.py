from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.logout, name="logout"),
    path('settings', views.settings, name="settings"),
    path('profile/<str:pk>', views.profile, name="profile"),
    path('upload', views.upload, name="upload"),
    path('like-post', views.like_post, name="like-post"),
    path('follow', views.follow, name="follow"),
    path('search', views.search, name="search"),
    path('contact', views.contact, name="contact"),
    path('terms', views.terms, name="terms"),
    path('policy', views.policy, name="policy"),
    path('about', views.about, name="about"),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name="password-reset.html"), name="password_reset"),
    path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(template_name="password-reset-sent.html"), name="password_reset_done"),
    path('reset-password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password-reset-form.html"), name="password_reset_confirm"),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-done.html"), name="password_reset_complete"),
]
