"""
URL configuration for jobberwax project.

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
from rest_framework.routers import DefaultRouter
from account.views import RegistrationViewSet, OrganisationUserViewset, OrganisationViewset
from jobs.views import PublicJobViewsets, JobViewset, ApplicationViewset

apiRouter = DefaultRouter(trailing_slash=False)
apiRouter.register(r"auth", RegistrationViewSet, basename="user-reg")
apiRouter.register(r"org-user", OrganisationUserViewset, basename="org-user")
apiRouter.register(r"org", OrganisationViewset, basename="org")
apiRouter.register(r"public/job", PublicJobViewsets, basename="public-job")
apiRouter.register(r"jobs", JobViewset, basename="job")
apiRouter.register(r"application", ApplicationViewset, basename="application")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((apiRouter.urls, "jobberwax"), namespace="api")),
]
