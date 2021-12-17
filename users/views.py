import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View

from users.models import User
from my_settings import SECRET_KEY


class SignupView(View):
    def post(self, request):
        data = json.loads(request.body)
        REGEX_PASSWORD = re.compile(
            "^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{4,}$"
        )
        password = data["password"]
        nickname = data["nickname"]

        if User.objects.filter(nickname=nickname).exists():
            return JsonResponse({"MESSAGE": "ALREADY EXISTED NICKNAME"}, status=400)

        if not REGEX_PASSWORD.match(data["password"]):
            return JsonResponse({"MESSAGE": "PASSWORD_ERROR"}, status=400)

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        decoded_password = hashed_password.decode("utf-8")

        User.objects.create(
            nickname=nickname,
            password=decoded_password,
            is_admin=data["is_admin"]
        )
        return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)

        try:
            if not User.objects.filter(nickname=data["nickname"]).exists():
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)

            user = User.objects.get(nickname=data["nickname"])

            if not bcrypt.checkpw(
                data["password"].encode("utf-8"), user.password.encode("utf-8")
            ):
                return JsonResponse({"MESSAGE": "INVALID_USER"}, status=401)
            
            access_token = jwt.encode({"id": user.id }, SECRET_KEY , algorithm="HS256")
            return JsonResponse({"MESSAGE": "SUCCESS", 'token' : access_token}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
