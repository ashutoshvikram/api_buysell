from django.shortcuts import render
from .models import Product,Users,Product_img,Message,Favourites,Profile
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .serializers import ProductSerializer,UsersSerializer,Product_imgSerializer,ProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from datetime import datetime
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_203_NON_AUTHORITATIVE_INFORMATION
)




# Create your views here.
@api_view(['GET'])

def prod_list(request):

       
        products=Product.objects.all()  
        for i in products:
            i.posted_on=i.posted_on.strftime('%d-%b,%Y') 
        serializer=ProductSerializer(products,many=True)
        return JsonResponse({'items':serializer.data,'message':'API WORKED SUCCESSFULLY','sname':'ashu'}, safe = False)

@csrf_exempt
@permission_classes((AllowAny,))
@api_view(['POST'])
def login(request):

    if request.method=='POST':
        
        email = request.data['email']
        password = request.data['password']
        
        try:
            temp=Users.objects.get(email=email,password=password)
        except Users.DoesNotExist:
            return JsonResponse({'success':False,'message':'Your credentials are incorrect'},
                                    status= HTTP_200_OK)
       
        request.session['name']=temp.firstname
        request.session['email']=email
        print('as')
        return JsonResponse({'sname': temp.firstname,'email':temp.email,'success':True},
                    status=HTTP_200_OK)
       
@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method=='POST':
        email=request.data['email']
        password=request.data['password']
        firstname=request.data['firstname']
        lastname=request.data['lastname']
        location=request.data['location']
        mobno=request.data['mobno']
        if Users.objects.filter(email=email).exists():
            return JsonResponse({'message':'You have already registerd','success':False})
        us=Users.objects.create(email=email,password=password,firstname=firstname,
                        lastname=lastname,location=location,Mobno=mobno)    
        return JsonResponse({'message':'User created','success':True})

def logout(request):
    if 'name' in request.session:
        print("######")
        print(request.session)
        del request.session['email']
        del request.session['name']
    # if 'name' not in request.session:
    #     print("logged out successfully")
    # d=a.auth_token.delete()
        return JsonResponse({'message':'You have logged out successfully'},status=HTTP_200_OK)
    else:
        print("********")
       
        
        return JsonResponse({'message':'You have not logged in ' })


@api_view(['POST'])

@csrf_exempt
def createaddid(request):
            if 'email' in request.session:
                p_name=request.data['p_name']
                p_description=request.data['p_description']
                p_category=request.data['p_category']
                p_price=request.data['p_price']
                p_location=request.data['p_location']
                seller=request.session['email']
                p_seller=Users.objects.get(email=seller)
        
                Prod_obj=Product(Product_name=p_name,Description=p_description
                ,Category=p_category,Price=p_price,Location=p_location,Seller_id=p_seller)
                Prod_obj.save()

       
                return JsonResponse({'message':'Your add is posted!!','id':Prod_obj.id},status=HTTP_200_OK)
            else:
                return JsonResponse({'message':'Please login to post add'},status=HTTP_200_OK)

class FileUploadView(APIView):
    parser_class = (MultiPartParser, FormParser)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
      if 'name' in request.session:
        print('in post')
        print('session b haui')
        print(request.data)
        file_serializer =  Product_imgSerializer(data=request.data)
          
        if file_serializer.is_valid():
            file_serializer.save()
            get_id=Product.objects.order_by('-id')[:1]
            fetchid=get_id[0].id
            imgobj=Product_img.objects.get(Product_id=fetchid)
            
            Product.objects.filter(id=fetchid).update(Image=imgobj.Product_images0)
            print(file_serializer)
        else:
            print('fault')
        return JsonResponse({'message':'you have done it'}, status=HTTP_200_OK)
      else:
        return Response(file_serializer.errors, status=HTTP_200_OK)



class ProfileUploadView(APIView):
    parser_class = (MultiPartParser, FormParser)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
      if 'name' in request.session:
        email=request.session['email']
        print('in post')
        print('session b haui')
        print   (request.data)
        file_serializer=ProfileSerializer(data=request.data)
       
        if file_serializer.is_valid():
            file_serializer.save()
            p_img=Profile.objects.order_by('-id')[:1]
            Users.objects.filter(email=email).update(Profile_pic=p_img[0].profilepix)
            Userdetails=Users.objects.filter(email=email)
            serializera=UsersSerializer(Userdetails,many=True)
            print(file_serializer)
        else:
            print('fault')
        return JsonResponse({'message':'you have done it','userdetails':serializera.data}, status=HTTP_200_OK)
      else:
        return Response(file_serializer.errors, status=HTTP_200_OK)

# Adds on the basis of category 
@csrf_exempt
def category(request):
    if 'email' in request.session:
        sname=request.session['name']
    else:
        sname=''
    category=request.GET['cat']
    products=Product.objects.filter(Category=category)
    for i in products:
            i.posted_on=i.posted_on.strftime('%d-%b,%Y') 
    serializer=ProductSerializer(products,many=True)
    return JsonResponse({'items':serializer.data,
                            'sname': sname},status=HTTP_200_OK)
# Adds on basis of location 
def location(request):
    if 'email' in request.session:
        sname=request.session['name']
    else:
        sname=''
    location=request.GET['loc']
    products=Product.objects.filter(Location=location)
    for i in products:
            i.posted_on=i.posted_on.strftime('%d-%b-%Y') 
    serializer=ProductSerializer(products,many=True)
    return JsonResponse({'items':serializer.data,
                            'sname': sname},status=HTTP_200_OK)

#Advertisement page   
@csrf_exempt
def adddetails(request,id):
    if 'email' in request.session:
        p_id=id
        print('******')
        print(p_id)
        prod=Product.objects.get(id=p_id)
        pro_images=Product_img.objects.filter(Product_id=p_id)
       
        imgserializer=Product_imgSerializer(pro_images,many=True)
        U_obj=Users.objects.get(email=prod.Seller_id.email)
        userserializer=UsersSerializer(U_obj)
        serializer=ProductSerializer(prod)
        
        return JsonResponse({'items':serializer.data,
                            'seller':userserializer.data,
                            'productimage':imgserializer.data,
                            'sname':request.session['name']},status=HTTP_200_OK)
    else:
        p_id=id
        prod=Product.objects.get(id=p_id)
        serializer=ProductSerializer(prod)
        img=Product_img.objects.filter(Product_id=p_id)
        imgserializer=Product_imgSerializer(img,many=True)
      
        return JsonResponse({'items':serializer.data,
          'productimage':imgserializer.data})
#user posted adds  
@csrf_exempt
def myadds(request):
    if 'email' in request.session:
        email=request.session['email']
        sname=request.session['name']
        user_obj=Users.objects.get(email=email)
        Productlist=Product.objects.filter(Seller_id=user_obj)
        serializer=ProductSerializer(Productlist,many=True)
        img=Product_img.objects.filter(Product_id=p_id)
        imgserializer=Product_imgSerializer(img,many=True)
        return JsonResponse({'items':serializer.data,'sname':sname})
    else:
        return JsonResponse({'message': 'Please login to see the page'})


def my_favourites(request):
    if 'email' in request.session:
        email=request.session['email']
        sname=request.session['name']
        user_obj=Users.objects.get(email=email)
        fav=Favourites.objects.filter(User_name=user_obj)
        ad=[]
        for i in fav:
            ad.append(Product.objects.get(id=i.id))
        serializer=ProductSerializer(ad,many=True)
        return JsonResponse({'items':serializer.data})
    
    else:
        return JsonResponse({'message': 'Please login to see the page'})



@api_view(['POST'])
@csrf_exempt
def contactus(request):
   
        if 'name' in request.session:
            sname=request.session['name']
        else:
            sname=""
        Email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message'] +"\n\n\n\n\n"+"From:-"+ Email
        mail = EmailMessage(
                    subject,
                    message,
                    Email,
                    ['avikram396@gmail.com']
                    
                    )
        mail.send()
        
        return JsonResponse({'message':'Thanks for the feedback','sname':sname})
   
@csrf_exempt
def profile(request):

    if 'name' in request.session:
        email=request.session['email']
        Userdetails=Users.objects.filter(email=email)
        serializera=UsersSerializer(Userdetails,many=True)
        return JsonResponse({'userdetails':serializera.data,'success':True})
    else:
      
        return JsonResponse({'message':'You have not logged in..'},status= HTTP_400_BAD_REQUEST)

def contactseller(request,id):
    if 'name' in request.session:
        email=request.session['email']
        p_id=id
        seller=Product.objects.get(id=p_id)
       
        message="Dear"+" "+seller.Seller_id.Firstname+"\n\n\n"+request.session.name+"is interested to buy your"+ seller.Product_name+"\n\n\n\n\n"+"From:-"+ email
        mail = EmailMessage(
                    subject,
                    message,
                    email,
                    [seller.Seller_id.email]
                    
                    )
        mail.send()
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})