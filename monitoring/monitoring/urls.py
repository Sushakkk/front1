"""
URL configuration for monitoring project.

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
from django.urls import path
from threats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.threats_list, name='threats_list'),
    path('threat/<int:id>/', views.threat_description, name='threat_description'),
    path('current/<int:id>/', views.threat_request, name='threat_request'),
    path('add-threat/', views.add_threat, name='add_threat'),
    path('del-threat/', views.del_request, name='del_request'),
]
