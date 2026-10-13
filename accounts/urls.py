from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # Email OTP
    path("send-email-otp/", views.send_email_otp, name="send_email_otp"),
    path("verify-email-otp/", views.verify_email_otp, name="verify_email_otp"),

    
    path("admin-dashboard/",views.admin_dashboard,name="admin_dashboard"),
    
    # My Profile
    path("profile/", views.profile_view, name="profile"),
]