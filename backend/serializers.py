from rest_framework import serializers
from .models import Product,Users,Product_img,Profile
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
class Product_imgSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Product_img
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['email','Mobno','location','Profile_pic','firstname','lastname','registered_on']

