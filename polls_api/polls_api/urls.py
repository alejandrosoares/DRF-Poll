"""polls_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework_swagger.views import get_swagger_view
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

swagger_schema = get_swagger_view(title='Polls API')

urlpatterns = [
    path('users/', include('users.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', swagger_schema)
]


# if settings.DEBUG:
#     from .settings.base import MEDIA_URL, MEDIA_ROOT
#     from django.conf.urls.static import static
#     urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)