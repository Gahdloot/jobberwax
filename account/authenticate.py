import datetime as d
import logging
from abc import ABC

import jwt
from django.contrib.auth import get_user_model
from account.models import User
from jobberwax.settings import API_ACCESS_SECRET, API_REFRESH_SECRET
from rest_framework import authentication, exceptions


User = get_user_model()


class APIAuthentication(authentication.BaseAuthentication, ABC):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if auth and len(auth) != 2:
            token = auth[0].decode("utf-8")
            try:
                payload = jwt.decode(token, API_ACCESS_SECRET, algorithms="HS256")
            except Exception as exc:
                raise exceptions.AuthenticationFailed(f"Token Expired: {exc}")
                # return Response({"status": False, "message": "Token Expired"}, status=401)
            user = self.get_user(payload["user_id"])
            return user, token
        raise exceptions.AuthenticationFailed("Invalid Authorization header format")

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            # if user.user_type == "Creative":
            #     user = Creative.objects.get(user=user)
            # elif user.user_type == "Partner":
            #     user = Partner.objects.get(user=user)
            # else:
            #     raise Exception("Cannot get User type of this user")
        except Exception as exc:
            logging.error(exc)
            raise Exception("User does not exist")
        return user


def create_refresh_token(user_id):
    return jwt.encode(
        {
            "user_id": user_id.hex,
            "exp": d.datetime.now() + d.timedelta(days=14),
            "iat": d.datetime.now(),
        },
        API_REFRESH_SECRET,
        algorithm="HS256",
    )


def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, API_REFRESH_SECRET, algorithms="HS256")
        return payload["user_id"]
    except Exception as exc:
        raise exceptions.AuthenticationFailed(f"unauthenticated: {str(exc)}")


def create_access_token(user_id):
    return jwt.encode(
        {
            "user_id": user_id.hex,
            "exp": d.datetime.now() + d.timedelta(minutes=35),
            "iat": d.datetime.now(),
        },
        API_ACCESS_SECRET,
        algorithm="HS256",
    )


def encode_email_to_jwt(email):
    token = jwt.encode(
        {"reset": email, "exp": d.datetime.now() + d.timedelta(minutes=30)},
         "TestABC123#",
        algorithm="HS256",
    )
    return token


def decode_email(token):
    key = jwt.decode(token, "TestABC123#", algorithms="HS256")
    return key