from django.contrib import admin
from .models import Users,Product_img,Product,Favourites,Message
# Register your models here.
admin.site.register(Users)
admin.site.register(Product)
admin.site.register(Product_img)
admin.site.register(Favourites)
admin.site.register(Message)