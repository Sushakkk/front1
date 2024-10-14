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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for the project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),

    path('admin/', admin.site.urls),
    

    path(r'threats/', views.ThreatList.as_view(), name='threats-list'),                             # список угроз (GET)
    path(r'threats/detail/', views.AddNewThreatView.as_view(), name='threats-create'),                     # добавление (POST), 
    path(r'threats/detail/<int:pk>/', views.ThreatDetail.as_view(), name='threats-delete'),            # удаление DELETE
    path(r'threats/detail/<int:pk>/', views.ThreatDetail.as_view(), name='threat-detail'),             # детальное описание угрозы (GET)
    path(r'threats/add/<int:pk>/', views.AddThreatView.as_view(), name='add-threat-to-request'), # добавление в заявку для пользователя
    path(r'threats/image/', views.ImageView.as_view(), name='add-image'),             # замена изображения

    #requests domain
    path(r'requests/',views.ListRequests.as_view(),name='list-requests-by-username'),
    path(r'requests/<int:pk>/',views.GetRequests.as_view(),name='get-request-by-id'),
    path(r'requests/<int:pk>/',views.GetRequests.as_view(),name='put-request-by-id'),
    
    path(r'requests/form/<int:pk>/',views.FormRequests.as_view(),name='form-request-by-id'),
    path(r'requests/moderate/<int:pk>/',views.ModerateRequests.as_view(),name='moderate-request-by-id'),
    path(r'requests/moderate/<int:pk>/',views.ModerateRequests.as_view(),name='delete-request-by-id'),

    #m-m
    path(r'request-threat/<int:pk>/',views.EditRequestThreat.as_view(),name='delete-from-request-by-id'),
    path(r'request-threat/<int:pk>/',views.EditRequestThreat.as_view(),name='add-price-request-by-id'),

    # user domain
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/profile/', views.UserUpdateView.as_view(), name='profile'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
]
