from django.db import models

# Create your models here.
class Users(models.Model):
    email=models.EmailField(max_length=40,unique=True,primary_key=True)
    password=models.CharField(max_length=25)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    location = models.CharField(max_length=30, blank=True)
    Image=models.ImageField(upload_to='profile',null=True)
    Mobno=models.CharField(max_length=14)
    Profile_pic=models.ImageField(upload_to='profile',null=True)
    registered_on=models.DateField(auto_now=True)

class Profile(models.Model):
    profilepix=models.ImageField(upload_to='test_profile' )    

class Product(models.Model):
    Product_name=models.CharField(max_length=60)
    Description=models.CharField(max_length=200)
    Category=models.CharField(max_length=100,null=True)
    posted_on=models.DateField(auto_now=True)
    Location=models.CharField(max_length=100)
    Price=models.DecimalField(max_digits=9,decimal_places=0)
    Seller_id=models.ForeignKey(Users,on_delete=models.CASCADE)
    Image=models.ImageField(upload_to="productimg",null=True)
    
class Product_img(models.Model):
    Product_id=models.CharField(max_length=4,primary_key=True)
    Product_images0=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images1=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images2=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images3=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images4=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images5=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images6=models.ImageField(upload_to="productimg/caraousel",null=True )
    Product_images7=models.ImageField(upload_to="productimg/caraousel",null=True )
    

class Message(models.Model):
    Sender=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='sender')
    Receiver=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='receiver')
    Message=models.CharField(max_length=500)

class Favourites(models.Model):
    User_name=models.ForeignKey(Users,on_delete=models.CASCADE)
    Product_key=models.ForeignKey(Product,on_delete=models.CASCADE)

