from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name = 'home'),
    path('register/', user_views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('accounts/profile/', user_views.profile, name = 'profile'),
    # path('upload/', user_views.DocumentCreateView.as_view(), name = 'upload'),
    path('upload/', user_views.file_upload, name = 'upload'),
    path('search/', user_views.search_user, name = 'search-user'),
    path('user/<username>', user_views.user_profile, name = 'user-profile'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
