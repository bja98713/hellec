from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from expertise import views  # 👈 L'import manquant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.accueil, name='accueil'),  # 👈 Ta vue d'accueil protégée par login
    path('', include('expertise.urls')),
]
