"""
URL configuration for lab3 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from monitoring import views 
from django.urls import include, path
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'threats/', views.ThreatList.as_view(), name='threats-list'),                         # список угроз (GET)
    path(r'threats/create/', views.ThreatDetail.as_view(), name='threats-create'),                     # добавление (POST), 
    path(r'threats/delete/<int:pk>/', views.ThreatDetail.as_view(), name='threats-delete'), 
    path(r'threats/<int:pk>/', views.ThreatDetail.as_view(), name='threat-detail'),             # детальное описание угрозы (GET), изменение (PUT), удаление (DELETE)
    path(r'threats/add/', views.AddThreatView.as_view(), name='add-threat-to-request'), # добавление в заявку для пользователя
    path(r'threats/image/', views.ImageView.as_view(), name='request-put'),             # добавление услуги в заявку

    #requests domain
    path(r'list-requests/',views.ListRequests.as_view(),name='list-requests-by-username'),

    # user domain
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('profile/', views.UserUpdateView.as_view(), name='profile'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
