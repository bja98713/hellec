# CEPN/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='personnels/', permanent=False), name='home'),
    path('', include('expertise.urls')),
]
