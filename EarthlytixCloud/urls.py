from django.contrib import admin
from django.urls import include, path
# from django.conf import settings

urlpatterns = [
    path('manageportal/', admin.site.urls),
    path('api/version=1/', include('waste_management.urls')),
]

