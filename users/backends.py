# 로그인할 때 이메일과 비밀번호로 로그인할 수 있게 하기위해서 제작
# 기존에는 authenticate 함수를 사용해서 로그인을 했는데 해당 함수는 username과 password를 이용해야만 로그인이 가능했다
# 로그인할 때 username으로 로그인하는게 별로라 생각하여 커스텀으로 authenticate 함수를 수정을 하였다

# 코드를 작성하고 setting에 백앤드 부분에 추가해줘야한다
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

class EmailAuthBackend(BaseBackend):
    def authenticate(self,request, email = None, password = None, **kwargs):
        try:
            user = User.objects.get(email = email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
        