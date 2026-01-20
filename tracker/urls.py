from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('show/<int:pk>/', views.show_detail, name='show_detail'),
    path('add/', views.add_show, name='add_show'),
    path('api/mark_watched/', views.mark_watched, name='mark_watched'),
]
