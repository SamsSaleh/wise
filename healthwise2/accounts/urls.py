from django.urls import path
from . import views
from .views import MyPasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
    path("", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("signup/", views.signup_request, name="signup"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  views.activate, name='activate'),
    path('reset-password/', MyPasswordResetView.as_view(), name='password_reset'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("password_reset_complete/", views.login_request, name="password_reset_complete"),
    path("reset-email-sent/", views.login_request, name="reset-email-sent"),
    path("change_password/", views.MyPasswordChangeView.as_view(), name="change_password")
]
