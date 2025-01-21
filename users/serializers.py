from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구
from django.contrib.auth.password_validation import validate_password # Django의 기본 pw 검증 도구
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import UserCredit

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = True, validators = [UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only = True, # 쓰기만 해야하는 필드
        required = True,
        validators = [validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username","email","password","password2"]

    def validate(self, data): # validate 데이터 검증 함수(자동 호출) password와 password2 일치 여부 확인하기 위해 제작
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password" : "Password fields didn't match."})
        return data
    
    def create(self, validated_data): # 회원가입 시 유저를 생성하고 토큰도 같이 생성한다
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        credit = UserCredit.objects.create(user = user, credit = 0)

        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required = True, write_only = True)

    class Meta:
        model = User
        fields = ["email","password"]

    def validate(self, data):
        user = authenticate(**data)
        
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError({"error" : "Unable to log in with provided credentials"})

class UserCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCredit
        fields = "__all__"