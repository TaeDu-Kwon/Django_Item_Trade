from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.

from .froms import ProductForm
import requests
import json

#User
from users.serializers import SignUpSerializer,LoginSerializer, UserCredit
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import UserCredit


API_PATH = "http://127.0.0.1:8001/"

# ---------------------------------------- 매인 페이지 관련 ------------------------------------------- #
def home_page(request):
    # 매인 페이지 관련 함수
    # item app에서 최근 등록된 5개 상품 찾아와 보여주도록 설정정
    path = "http://127.0.0.1:8001/products/get-recently-create-item"
    items = {}
    
    res = requests.get(path)
    items = res.json()
    
    table_data = {
        "account_data" : items["account_data"],
        "item_data" : items["item_data"],
        "game_money_data" : items["game_money_data"]
    }
    
    return render(request,"item_trade_page/home_page.html",{"user" : request.user,"table_data":table_data})

def login_page(request):
    # 로그인 페이지 관련 함수
    if request.method == "POST":
        serializer = LoginSerializer(data = request.POST)

        if serializer.is_valid():
            token = serializer.validated_data
            user = User.objects.get(auth_token = token)
            # 이메일로 로그인하기 위해서 백앤드 부분을 제작함함
            user.backend = 'users.backends.EmailAuthBackend' # 제작한 백앤드 설정
            login(request, user)
            return redirect("item_trade:home_page")
        else:
            for error in serializer.errors.values():
                print(error[0])
                messages.error(request, error[0])

    return render(request,"item_trade_page/login_page.html")

def signup_page(request):
    # 회원가입 페이지 관련 함수수
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
def logout_view(request):
    # 로그아웃
    logout(request)
    return redirect("item_trade:home_page")

# ---------------------------------------- 상품 등록 관련 ------------------------------------------- #

@login_required # 로그인이 필요한 뷰
def create_product_view(request):
    # 상품 등록 관련 함수
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
        
        if respone.status_code == 201:
            return redirect("item_trade:home_page")  

    return render(request, 'item_trade_page/create_product.html', {'form': form})

# ---------------------------------------- 상품 상세페이지 및 상품 구매매 관련 ------------------------------------------- #
@login_required # 로그인이 필요한 뷰
def product_info_page(request,product_type,product_id):
    # 상품 상세페이지 관련 함수
    respone = requests.get(API_PATH+"products/get-product-info/{}/{}".format(product_type,product_id))
    product_data = respone.json()
    

    return render(request, "item_trade_page/product_info_page.html",product_data)

@login_required # 로그인이 필요한 뷰
def product_purchase_page(request,product_type,product_id):
    # 결제 페이지 관련 함수 
    respone = requests.get(API_PATH+"products/get-product-info/{}/{}".format(product_type,product_id))
    product_data = respone.json()

    # 최종 결제 함수에서 데이터 사용하기 위해서 session에 저장한다
    request.session["product_data"] = product_data 

    return render(request, "item_trade_page/product_purchase_page.html",product_data)

@login_required # 로그인이 필요한 뷰
def buy_the_product(request): 
    # 상품 최종 결제 함수
    if request.method == "POST":
        product_data = request.session.get("product_data")["product_data"][0]
        product_id = product_data["id"]
        product_type = product_data["product_type"]

        api_url = API_PATH + "products/buy-product/"
        headers = {"Content-Type": "application/json"}
        data = {
            "product_id" : product_id,
            "product_type" : product_type,
            "user_id" : request.user.id
        }
        
        respone = requests.post(api_url, headers=headers , data=json.dumps(data, ensure_ascii=False))

        if respone.status_code == 200:
            return redirect("item_trade:home_page") 
        else:
            error_message = respone.json()
            return render(request, "item_trade_page/payment_fail.html", {"error": error_message})
        
@login_required # 로그인이 필요한 뷰
def payment_fail(request):
    # 최종 결제할 때 크레딧 부족으로 실패할 경우 보여주기 위한 페이지지
    return render(request, "item_trade_page/payment_fail.html", {"error": "사용자 크레딧이 부족합니다."})

# ---------------------------------------- 크레딧 결제 관련 ------------------------------------------- #
@login_required # 로그인이 필요한 뷰
def credit_page(request,user_id):
    # 크레딧 충전 페이지
    user_credit = UserCredit.objects.get(user__id= user_id)

    return render(request, "item_trade_page/credit_page.html",{"user_credit":user_credit})

@login_required # 로그인이 필요한 뷰
def kakaopay(request,user_name):
    # 크레딧 충전을 하기위해 카카오페이 api를 사용하여 충전하도록 제작작
    if request.method == 'POST':
        credit = int(request.POST.get('credit', 0))

        if credit < 5:
            return render(request, 'payFail.html')

        total_amount = credit * 1000
        
        admin_key = 'DEV8038EAA952F7A2BA70FE945F590AB63779A1D'
        url = f'https://open-api.kakaopay.com/online/v1/payment/ready'
        headers = {
            'Authorization': f'SECRET_KEY {admin_key}',
            "Content-Type": "application/json"
        }

        data = {
            'cid': 'TC0ONETIME', # 테스트용 CID, 상용은 발급받은 CID 사용
            'partner_order_id':'order_id_12345',  # 고유 주문 ID
            'partner_user_id': user_name, # 사용자 ID
            'item_name':'Creadit',
            'quantity': credit,  # 수량 (0이 아닌 양수)
            'total_amount': int(total_amount), # 총 가격
            'vat_amount': 200, # 부가세
            'tax_free_amount': 0, # 비과세
            'approval_url':'http://127.0.0.1:8001/paySuccess/', 
            'fail_url':'http://127.0.0.1:8001/payFail',
            'cancel_url':'http://127.0.0.1:8001/payCancel'
        }

        res = requests.post(url, data=json.dumps(data, ensure_ascii=False), headers=headers)

        result = res.json()
        request.session['tid'] = result['tid']
        request.session["user"] = data["partner_user_id"]
        request.session["credit"] = data["quantity"]
        return redirect(result['next_redirect_pc_url'])
     
    return render(request, "item_trade_page/payFail.html")  

def paySuccess(request):
    admin_key = 'DEV8038EAA952F7A2BA70FE945F590AB63779A1D'
    url = 'https://open-api.kakaopay.com/online/v1/payment/approve'
    headers = {
        'Authorization': f'SECRET_KEY {admin_key}',
        "Content-Type": "application/json"
    }
    data = {
        'cid':'TC0ONETIME',
        'tid': request.session['tid'],
        'partner_order_id':'order_id_12345',
        'partner_user_id': request.session['user'],
        'pg_token': request.GET['pg_token']
    }
    res = requests.post(url, data=json.dumps(data, ensure_ascii=False), headers=headers)
    result = res.json()

    if result.get('msg'):
        return redirect('/payFail')
    else:
        user = User.objects.get(username = request.session['user'])
        UserCredit.objects.update(user = user, credit = request.session["credit"])
        return redirect("item_trade:home_page")  
    
def payFail(request):
    return render(request, 'payFail.html')
def payCancel(request):
    return render(request, 'payCancel.html')

def my_page(request):
    # 마이페이지 관련 함수
    res = requests.get(API_PATH + "products/purchases/{}".format(request.user.id))
    user_credit = UserCredit.objects.get(user__id= request.user.id)
    purchase_record = res.json()

    return render(request, "item_trade_page/my_page.html",{"user":request.user,"purchase_record" : purchase_record, "user_credit" : user_credit})
