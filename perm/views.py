from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
)
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from utils.jwt_token import token_decoder
from django.urls import reverse
from django.core.mail import EmailMessage
from utils.email import EmailThread
from utils.jwt_token import token_generator
from .serializers import (
    RegisterSerializer,
    SeasonTokenObtainPairSerializer,
    ResendEmailVerificationSerializer,
    ChangePasswordSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer,
    ProfileSerializer,
    ProfileImageUploadSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView

import os
from datetime import datetime


User = get_user_model()


class RegisterAPIView(CreateAPIView):
    """회원가입 View"""

    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class SeasonTokenObtainPairView(TokenObtainPairView):
    # serializer_class에 커스터마이징된 시리얼라이저를 넣어 준다.
    serializer_class = SeasonTokenObtainPairSerializer
#class LoginAPIView(APIView):
#    """로그인 (토큰 저장) View"""
#
#    def post(self, request, format=None):
#        data = request.data
#        response = Response()        
#        user_id = data.get('user_id', None)
#        password = data.get('password', None)
#        user = authenticate(user_id=user_id, password=password)
#        if user is not None:
#            if user.is_active:
#                data = token_generator(user)
#                response.set_cookie(
#                                    key = settings.SIMPLE_JWT['AUTH_COOKIE'], 
#                                    value = data["access"],
#                                    expires = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
#                                    secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
#                                    httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
#                                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
#                                )
#                csrf.get_token(request)
#                response.data = {"message" : "로그인 완료","data":data}
#                
#                return response
#            else:
#                return Response({"message" : "이메일 인증이 완료되지 않은 계정입니다."}, status=status.HTTP_404_NOT_FOUND)
#        else:
#            return Response({"error": "잘못된 아이디 또는 비밀번호입니다."}, status=status.HTTP_404_NOT_FOUND)


class EmailVerificationAPIView(APIView):
    """이메일 인증 View"""

    def get(self, request, token):
        user_id = token_decoder(token)

        try:
            user = get_object_or_404(User, pk=user_id)
            if user.is_verified:
                return Response(
                    {"message": "이미 인증되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.is_active = True
            user.is_verified = True
            user.save()
            return Response(
                {"message": "이메일 인증이 완료되었습니다."},
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"error": "인증 링크가 잘못되었습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except TypeError:
            return Response(user_id)


class ResendEmailVerificationAPIView(APIView):
    """이메일 주소 인증 메일 재전송 View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = ResendEmailVerificationSerializer

    def post(self, request):
        serializer = ResendEmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            # 토큰 생성
            token = token_generator(user)

            confirm_url = self.request.build_absolute_uri(
                reverse("confirm_email", kwargs={"token": token["access"]})
            )
            #msg = f"이메일 인증 링크: {confirm_url}"
            msg = f"""\
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                    <title>[Find Me] 이메일 주소를 인증해주세요.</title>
                </head>
                <body>
                    <center class="wrapper">
                        <table class="main" width="100%">
                            <tr>
                                <td style="padding: 20px">
                                    <div>
                                        <center><h1>환영합니다!</h1></center>
                                        <p>
                                            "{user.email}" 이메일 주소로 계정 생성이 거의 완료되었습니다.<br>
                                            아래 링크를 눌러 이메일 주소를 인증하여 회원가입을 완료하세요.
                                        </p>
                                        <p>
                                            <a href="{confirm_url}">이메일 주소 인증하기</a>
                                        </p>
                                        <p>
                                            본인의 요청이 아닌 경우, 본 이메일을 무시하시면 되며 아무 일도 일어나지 않습니다.
                                        </p>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </center>
                </body>
            </html>
            """
            email_obj = EmailMessage("[Find Me] 이메일 주소를 인증해주세요.", msg, to=[user.email])
            email_obj.content_subtype = "html"

            EmailThread(email_obj).start()
            return Response(
                {"message: 인증 메일이 재전송되었습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """초기화 후 비밀번호 변경 View"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():

            user: User = User.objects.get(id=self.request.user.id)
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "비밀번호가 변경되었습니다."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response({"error": "잘못된 비밀번호입니다. 다시 시도하거나 비밀번호 찾기를 클릭하여 재설정하세요."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    """비밀번호 재설정 View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user: User = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {"error": "존재하지 않는 계정입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # 토큰 생성
            token = token_generator(user)

            set_password_url = self.request.build_absolute_uri(
                reverse("set_password", kwargs={"token": token["access"]})
            )
            #msg = f"비밀번호 재설정 링크: {set_password_url}"
            msg = """\
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                    <head>
                        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                        <title>[Find Me] 비밀번호 재설정 링크입니다.</title>
                    </head>
                    <body>
                        <center class="wrapper">
                            <table class="main" width="100%">
                                <tr>
                                    <td style="padding: 20px">
                                        <div>
                                            <center><h1>비밀번호 변경</h1></center>
                                            <p>
                                                비밀번호 변경 링크입니다.<br>
                                                비밀번호 변경하기 링크를 눌러 비밀번호를 변경해주세요.
                                            </p>
                                            <p>
                                                <a href="%s">비밀번호 변경하기</a>
                                            </p>
                                            <p>
                                                본인의 요청이 아닌 경우, 본 이메일을 무시하시면 되며 아무 일도 일어나지 않습니다.
                                            </p>
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </center>
                    </body>
                </html>
                """ % (user.user_id, user.email, set_password_url)
            email_obj = EmailMessage("[Find Me] 비밀번호 재설정 링크입니다.", msg, to=[user.email])
            email_obj.content_subtype = "html"

            EmailThread(email_obj).start()
            return Response(
                {"message: 비밀번호 재설정 메일이 전송되었습니다."},
                status=status.HTTP_200_OK,
            )

        return Response("")


class SetPasswordAPIView(APIView):
    """비밀번호 설정 View"""

    permission_classes = [permissions.AllowAny]
    serializer_class = SetPasswordSerializer

    def post(self, request, token):
        serializer = SetPasswordSerializer(data=request.data)
        user_id = token_decoder(token)

        try:
            user = get_object_or_404(User, pk=user_id)
        except Http404:
            return Response(
                {"error": "인증 링크가 잘못되었습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # 토큰 잘못됨/만료
        except TypeError:
            return Response(user_id)

        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "비밀번호가 변경되었습니다."},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileAPIView(RetrieveAPIView):
    """유저 프로필 View"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_object_or_404(User, id=self.get_object().id)


class ProfileImageUploadAPIView(APIView):
    """유저 프로필 이미지 업로드 View"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileImageUploadSerializer

    def post(self, request, format=None):
        user = request.user
        serializer = ProfileImageUploadSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid(raise_exception=True):
            if serializer.validated_data['profile_image'].size > 307200:
                response = {
                    'message': '프로필 이미지의 크기가 300KB를 초과합니다.'
                }
                return Response(response, status=status.HTTP_406_NOT_ACCEPTABLE)

            name = serializer.validated_data['profile_image'].name
            file_name, ext = os.path.splitext(name)
            now = datetime.now()
            date_time = now.strftime("%Y%m%d%H%M%S")
            custom_file_name = file_name + "_" + date_time + ext
            serializer.validated_data['profile_image'].name = custom_file_name
            
            serializer.save()
            return Response({
                'message': '프로필 사진이 설정됐습니다.',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)


class ProfileImageResetAPIView(APIView):
    """기본 프로필 이미지로 변경 View"""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, format=None):
        user = request.user
        default_profile = 'profile_images/default.png'
        
        user.profile_image = default_profile
        user.save()

        return Response({
            'message': '프로필 사진이 기본 이미지로 재설정되었습니다.',
            'data': ProfileImageUploadSerializer(user).data
        }, status=status.HTTP_200_OK)
