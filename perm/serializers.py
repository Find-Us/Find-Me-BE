from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from utils.email import EmailThread
from utils.jwt_token import token_generator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입 & 이메일 주소 인증 메일 전송 Serializer"""

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    user_id = serializers.RegexField(
        regex=r'^[a-zA-Z0-9]+$',
        max_length=30,
        min_length=6,
        required=True
    )
    name = serializers.RegexField(
        regex=r'^[ㄱ-ㅎ가-힣a-zA-Z0-9]+$',
        max_length=16,
        min_length=2,
        required=True
    )
    birth = serializers.DateField(required=True)

    def validate(self, attrs):
        password = attrs.get("password")

        if password != attrs["confirm_password"]:
            error = serializers.ValidationError({"error": "비밀번호가 일치하지 않습니다."})
            raise error

        try:
            validate_password(password)

        except serializers.ValidationError:
            raise serializers.ValidationError()
        return super().validate(attrs)

    # 회원가입
    def create(self, validated_attrs):
        request = self.context.get("request")
        email = validated_attrs.get("email").lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "이미 해당 이메일 주소를 사용하는 계정이 존재합니다."})
        user = User.objects.create_user(
            password=validated_attrs["password"],
            email=validated_attrs["email"],
            user_id=validated_attrs["user_id"],
            name=validated_attrs["name"],
            birth=validated_attrs["birth"]
        )
        # 토큰생성
        token = token_generator(user)

        confirm_url = request.build_absolute_uri(
            reverse("confirm_email", kwargs={"token": token["access"]})
        )
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
                                        "{email}" 이메일 주소로 계정 생성이 거의 완료되었습니다.<br>
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
        email_obj = EmailMessage("[Find Me] 이메일 주소를 인증해주세요.", msg, to=[email])
        email_obj.content_subtype = "html"

        EmailThread(email_obj).start()

        return {
            "id": user.id,
            "user_id": user.user_id,
            "name": user.name,
            "birth": user.birth,
            "email": user.email,
        }

    class Meta:
        model = User
        fields = ("id", "user_id", "name", "birth", "email", "password", "confirm_password")


class SeasonTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
		# 토큰 생성
        token = super().get_token(user)

        token['id'] = user.id
        token['user_id'] = user.user_id
        token['email'] = user.email

        return token


class ResendEmailVerificationSerializer(serializers.Serializer):
    """이메일 주소 인증 메일 재전송 Serializer"""

    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "존재하지 않는 계정입니다."})
        if user.is_verified:
            raise serializers.ValidationError({"error": "이미 인증되었습니다."})

        attrs["user"] = user
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """비밀번호 변경 Serializer"""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "비밀번호가 일치하지 않습니다."})

        try:
            validate_password(new_password)

        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """비밀번호 재설정 Serializer"""

    email = serializers.EmailField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    """비밀번호 초기화 후 설정 Serializer"""

    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"error": "비밀번호가 일치하지 않습니다."})

        try:
            validate_password(new_password)

        except serializers.ValidationError:
            raise serializers.ValidationError()

        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    """유저 프로필 Serializer"""

    class Meta:
        model = User
        fields = (
            'id',
            'profile_image',
            'user_id',
            'email',
            'name',
            'birth',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser',
        )


class ProfileImageUploadSerializer(serializers.ModelSerializer):
    """유저 프로필 이미지 업로드 Serializer"""

    class Meta:
        model = User
        fields = ['profile_image']
