from django.contrib import admin
from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('api', views.prod_list),
    path('api/login',views.login),
    path('api/signup',views.signup),
    path('api/logout',views.logout),
    path('api/postadd/id',views.createaddid),
    path('api/postadd',FileUploadView.as_view()),
    path('api/category',views.category),
    path('api/location',views.location),
    path('api/post/<str:id>',views.adddetails),
    path('api/myadds',views.myadds),
    path('api/favourites',views.my_favourites),
    path('api/profilepic',ProfileUploadView.as_view()),
    path('api/profile',views.profile),
    path('api/contactus',views.contactus),
    path('api/contactseller/:id',views.contactseller)
]
