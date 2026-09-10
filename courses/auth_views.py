from django.contrib.auth import get_user_model
from django.utils.crypto import constant_time_compare
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.utils import get_md5_hash_password

from .throttles import LoginRateThrottle


class SessionRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        token = self.token_class(attrs['refresh'])
        user = get_user_model().objects.filter(pk=token.get(api_settings.USER_ID_CLAIM)).first()
        if not user or not user.is_active or not constant_time_compare(
            token.get(api_settings.REVOKE_TOKEN_CLAIM, ''), get_md5_hash_password(user.password)
        ):
            raise AuthenticationFailed('Сессия недействительна. Войдите снова.')
        return super().validate(attrs)


class LoginView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]


class RefreshView(TokenRefreshView):
    serializer_class = SessionRefreshSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'refresh'


class LogoutView(TokenBlacklistView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'logout'
