from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

from .froms import ProductForm
import requests

#User
from users.serializers import SignUpSerializer,LoginSerializer
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from items.models import Game

API_PATH = "http://127.0.0.1:8001/"

def home_page(request):
    path = "http://127.0.0.1:8001/products/get-recently-create-item"
    items = {}
    
    res = requests.get(path)
    items = res.json()
    print(items)
    table_data = {
        "account_data" : items["account_data"],
        "item_data" : items["item_data"],
        "game_money_data" : items["game_money_data"]
    }
    
    return render(request,"item_trade_page/home_page.html",{"user" : request.user,"table_data":table_data})

def login_page(request):
    if request.method == "POST":
        serializer = LoginSerializer(data = request.POST)

        if serializer.is_valid():
            token = serializer.validated_data
            user = User.objects.get(auth_token = token)
            user.backend = 'users.backends.EmailAuthBackend' # 제작한 백앤드 설정
            login(request, user)
            return redirect("item_trade:home_page")
        else:
            for error in serializer.errors.values():
                print(error[0])
                messages.error(request, error[0])

    return render(request,"item_trade_page/login_page.html")

def signup_page(request):
    if request.method == "POST":
        serializer = SignUpSerializer(data = request.POST)
        
        if serializer.is_valid():
            user = serializer.save()
            messages.success(request, "회원가입 성공하였습니다.")
            login(request, user)
            return redirect("item_trade:home_page")
        else:
            for error in serializer.errors.values():
                messages.error(request, error[0])
    
    return render(request, "item_trade_page/signup_page.html")

def logout_view(request):
    logout(request)
    return redirect("item_trade:home_page")

@login_required # 로그인이 필요한 뷰
def create_product_view(request):
    form = ProductForm()  # 기본 폼

    if request.method == "POST":
       
        selected_game = request.POST.get("game")
        user = request.user.id
        product_type = request.POST.get("product_type")

        data = {
            "game" : selected_game,
            "title" : request.POST.get("title"),
            "seller" : user,
            "product_type" : product_type,
            "description" : request.POST.get("description"),
        }
      
        if product_type == "account": 
            data["account_class"] = request.POST.get("account_class")
            data["price"] = request.POST.get("price")
        
        elif product_type == "item":
            data["item_name"] = request.POST.get("item_name")
            data["quantity"] = request.POST.get("quantity")
            data["price_per_item"] = int(request.POST.get("price_per_item"))
        
        elif product_type == "game_money":
            data["total_amount"] = request.POST.get("total_amount")
            data["total_price"] = request.POST.get("total_price")

        # 이미지 넘기기기
        files = []
        if request.FILES.getlist('images'):
            for image in request.FILES.getlist('images'):
                files.append(('product_image', image))

        respone = requests.post(API_PATH+"products/create/",data=data, files=files)
        print(respone.json())
        if respone.status_code == 201:
            return redirect("item_trade:home_page")  

    return render(request, 'item_trade_page/create_product.html', {'form': form})

@login_required # 로그인이 필요한 뷰
def product_info_page(request,product_type,product_id):
    respone = requests.get(API_PATH+"products/get-product-info/{}/{}".format(product_type,product_id))
    product_data = respone.json()
    print(product_data)

    return render(request, "item_trade_page/product_info_page.html",product_data)

@login_required # 로그인이 필요한 뷰
def product_purchase_page(request,product_type,product_id):
    respone = requests.get(API_PATH+"products/get-product-info/{}/{}".format(product_type,product_id))
    product_data = respone.json()

    return render(request, "item_trade_page/product_purchase_page.html",product_data)

def kakaopay(request):
    pass