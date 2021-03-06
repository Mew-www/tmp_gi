"""gi_assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.shortcuts import render
from django.views.generic import TemplateView


urlpatterns = [
    path('nondefaultadminsite/', admin.site.urls),
    path('intentionallybroken/', render),

    path('reporting/v1/', include('reporting.urls.v1')),
    path('', TemplateView.as_view(template_name='backend_test_ui.html'))
]


def request_404(request, exception=None):
    return render(request, '404.html', status=404)


handler404 = request_404


def request_500(request, exception=None):
    return render(request, '50x.html', status=500)


handler500 = request_500
