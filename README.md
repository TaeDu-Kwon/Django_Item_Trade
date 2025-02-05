## Django Item Trade

## **개요**
이 프로젝트는 Django와 Django REST Framework(DRF)를 사용하여 구축된 아이템 거래 웹사이트입니다. 
게임 아이템 거래사이트를 모티브로 하여 제작하여 사용자 인증, 아이템 거래, 장바구니 기능 및 게임 내 화폐 거래 기능을 제공합니다.

## **기슬 스택**
Python 
Django
Html
Rest Framework

## **주요 기능**
- **`사용자 인증`**: 회원가입, 로그인 및 계정 관리
- **`크레딧 시스템`**: 크레딧을 충전하여 이를 통해 상품 구매 가능합니다.
- **`카카오페이 결제`**: 카카오페이 Open API를 이용하여 결제 기능을 사용하여 크레딧을 구매 합니다.
- **`안전한 거래`**: 저장된 크레딧을 이용하여 안전하게 구매할 수 있습니다.
- **`상품 등록`**: 계정, 게임 아이템, 게임 머니 상품을 등록할 수 있습니다.
- **`장바구니 기능`**: 원하는 아이템을 내 장바구니에 추가 및 삭제하여 구매하고 싶은 상품을 관리할 수 있습니다.
- **`개인 페이지`**: 사용자의 크레딧 및 구매 내력을 확인할 수 있습니다.

## **서버 실행**
**py manage.py runserver 8001**

**python3 manage.py runserver 8001**


## 프로젝트 구조
### 1. **User 앱**
사용자 인증 및 크레딧 관리를 담당합니다.

- **모델**:
  - `UserCredit`: 사용자 크레딧 정보를 저장.

- **시리얼라이저**:
  - `SignUpSerializer`: 회원가입 처리.
  - `LoginSerializer`: 로그인 및 토큰 인증 관리.

- **뷰**:
  - `SignUpView`: 회원가입 처리.
  - `LoginView`: 사용자 인증 및 토큰 반환.

### 2. **Item 앱**
게임 관련 아이템, 계정 및 게임 머니 거래를 관리합니다.

- **모델**:
  - `Game`: 게임 정보 저장.
  - `Product`: 아이템의 기본 클래스(추상 클래스).
  - `AccountProduct`, `ItemProduct`, `GameMoneyProduct`: 각기 다른 상품 모델.
  - `ProductImage`: 상품 이미지 저장.
  - `PurchaseRecord`: 구매 기록 저장.

- **시리얼라이저**:
  - 모든 상품 모델, 게임 및 구매 기록을 위한 시리얼라이저 제공.

- **뷰**:
  - `CreateProductView`: 사용자가 아이템을 등록할 수 있음.
  - `ProductViewsets`: 상품 정보를 조회하고 구매할 수 있음.

### 3. **Shopping Cart 앱**
사용자가 장바구니에 아이템을 추가/삭제할 수 있도록 관리합니다.

- **모델**:
  - `Cart`: 사용자별 장바구니 저장.
  - `CartItem`: 장바구니 내 아이템 저장.

- **시리얼라이저**:
  - `CartSerializer`: 장바구니 데이터 직렬화.
  - `CartItemSerializer`: 장바구니 아이템 데이터 직렬화.

- **뷰**:
  - `CartViewSet`: 사용자의 장바구니 관리.
  - `CartItemViewSet`: 장바구니 아이템 추가/삭제.

### 4. **Item Trade Page 앱**
HTML 페이지 렌더링 및 사용자 상호작용을 담당합니다.


## API 엔드포인트

### **사용자 API**
| 메서드 | 엔드포인트 | 설명 |
|--------|---------|-------------|
| POST | `/signup/` | 사용자 회원가입 |
| POST | `/login/` | 사용자 로그인 |

### **아이템 API**
| 메서드 | 엔드포인트 | 설명 |
|--------|---------|-------------|
| POST | `/create/` | 새로운 상품 등록 |
| GET | `/get-recently-create-item/` | 최근 등록된 아이템 조회 |
| GET | `/get-product-info/<str:product_type>/<int:product_id>/` | 특정 상품 정보 조회 |
| POST | `/buy-product/` | 상품 구매 |

### **장바구니 API**
| 메서드 | 엔드포인트 | 설명 |
|--------|---------|-------------|
| GET | `/cart/` | 사용자 장바구니 조회 |
| POST | `/cart-items/` | 장바구니에 아이템 추가 |
| DELETE | `/cart-items/<int:user_id>/<int:product_id>/<str:product_type>/` | 장바구니에서 아이템 삭제 |

## 결제 연동 (KakaoPay)
사용자는 KakaoPay를 통해 크레딧을 충전하고 상품을 구매할 수 있습니다.

### KakaoPay 결제 과정
1. 사용자가 크레딧 충전 금액을 선택.
2. 시스템이 KakaoPay API에 결제 요청 전송.
3. 사용자가 KakaoPay 결제 페이지로 리디렉션됨.
4. 결제가 완료되면 사용자의 계정에 크레딧이 추가됨.



