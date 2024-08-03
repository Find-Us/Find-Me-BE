from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings


class CustomRefreshToken(RefreshToken):
    """커스텀 refresh token"""

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["user_id"] = user.user_id
        token["email"] = user.email
        return token


def token_generator(user):
    """토큰 생성"""
    refresh = CustomRefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def token_decoder(token):
    """토큰 복호화"""
    try:
        decoded_data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_data["id_claim"]
    
    except jwt.ExpiredSignatureError:
        return {
            "error": "이메일 주소 인증 링크가 만료되었습니다.",
        }
    
    except jwt.InvalidTokenError:
        return {
            "error": "이메일 주소 인증 링크가 유효하지 않습니다.",
        }
