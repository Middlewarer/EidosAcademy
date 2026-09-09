import hashlib

from rest_framework.throttling import SimpleRateThrottle

def hash_identity(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class LoginRateThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        ip_address = self.get_ident(request)
        username = str(
            request.data.get("username", "")
        ).strip().lower()

        identity = f"{ip_address}:{username}"

        return self.cache_format % {
            "scope": self.scope,
            "ident": hash_identity(identity),
        }


class RegisterRateThrottle(SimpleRateThrottle):
    scope = "register"

    def get_cache_key(self, request, view):
        ip_address = self.get_ident(request)

        return self.cache_format % {
            "scope": self.scope,
            "ident": ip_address,
        }


class PasswordRateThrottle(SimpleRateThrottle):
    scope = "password"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": request.user.pk,
        }


class FeedbackRateThrottle(SimpleRateThrottle):
    scope = "feedback"

    def get_cache_key(self, request, view):
        return self.cache_format % {
            "scope": self.scope,
            "ident": self.get_ident(request),
        }
