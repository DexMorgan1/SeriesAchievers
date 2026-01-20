from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # The built-in admin panel
    path('admin/', admin.site.urls),
    
    # This tells Django to look at your 'tracker' app for all other pages
    path('', include('tracker.urls')),
]
