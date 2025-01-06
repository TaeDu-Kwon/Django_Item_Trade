from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

from .froms import ProductForm
import requests

#User
from users.serializers import SignUpSerializer,LoginSerializer
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from items.models import Game

API_PATH = "http://127.0.0.1:8001/"

def home_page(request):
    # path = "http://127.0.0.1:8001/products/get-recently-create-item/account"
    # try:
    #     res = requests.get(path)
    #     items = res.json()
    #     print(1)
    #     print(items)
    #     print(2)
    # except:
    #     pass
    return render(request,"item_trade_page/home_page.html",{"user" : request.user})

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

@login_required # 로그인이 필요한 뷰
def create_product_view(request):
    form = ProductForm()  # 기본 폼

    if request.method == "POST":
       
        selected_game = request.POST.get("game")
        game = Game.objects.get(pk = int(selected_game))
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

        respone = requests.post(API_PATH+"products/create/",data)
        print("----------")
        print(data)
        print("---------")
        print(respone.json())
        print("----------")
        if respone.status_code == 201:
            return redirect("item_trade:home_page")  

    return render(request, 'item_trade_page/create_product.html', {'form': form})


