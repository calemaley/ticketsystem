"""
URL configuration for ticketsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from users import views as user_view
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from events import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('events.urls')),
    path('register/', user_view.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name = 'user-login'),
    path('reset_password/', user_views.reset_password, name="reset_password"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('logout/',views.logout_user,name='logout'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
     
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
