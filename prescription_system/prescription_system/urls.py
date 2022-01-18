"""prescription_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drugs.urls import router as drugs_router
from django.urls import include, re_path
from prescriptions.urls import router as prescriptions_router
from users.urls import router as users_router
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include((drugs_router.urls, 'drugs'))),
    re_path('', include((prescriptions_router.urls, 'prescriptions'))),
    re_path('', include((users_router.urls, 'users')))
]
