import logging
from django.contrib.auth import hashers
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from account.models import User, Organisation, OrganisationUser
from account.authenticate import create_access_token, create_refresh_token
from account.serializer import UserSerializer
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from swagger.api_request import (
    login_request,
    login_response,
    signup_request,
    signup_response
)



class RegistrationViewSet(ViewSet):
    authentication_classes = []

    #url path is set to create
    # @extend_schema(request=signup_request, responses=signup_response)
    @swagger_auto_schema(method='post', request_body=signup_request, responses=signup_response)
    @action(detail=False, methods=['post'], url_path='create')
    def custom_create(self, request):
        payload = request.data

        #check that email is not non or blank
        if payload.get("email") is not None and isinstance(payload.get("email"), str) and len(payload.get("email")) > 4:
            #check that mail doesn't exists
            if User.objects.filter(email=payload.get("email")).exists():
                return Response(
                    data={
                        "code": 5,
                        "status": False,
                        "data": {"message": "User with this email already exists"},
                    },
                    status=401,
                )
            required_field = ["password", "first_name", "last_name"]
            #check that other fields is not non or blank
            for field in required_field:
                if payload.get(field) is None or len(payload.get(field)) < 3 or isinstance(payload.get("email"), str) is False:
                    return Response(
                    data={
                        "code": 5,
                        "status": False,
                        "data": {"message": f"Invalid {field} field"},
                    },
                    status=401,
                )
            user = User(
                email=payload.get("email"),
                password=hashers.make_password(payload.get("password")),
                first_name=payload.get("first_name"),
                last_name=payload.get("last_name")
            )
            user.save()
            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)
            response = Response()
            response.set_cookie(
                key="refreshToken",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            response.set_cookie(
                key="accessToken",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="None",
            )
            response.data = {"token": access_token, "user": UserSerializer(user).data}
            response.status_code = 200
            return response
        return Response(
                    data={
                        "code": 5,
                        "status": False,
                        "data": {"message": "Invalid Email field"},
                    },
                    status=401,
                )
    @swagger_auto_schema(method='post', request_body=login_request, responses=login_response)
    # @extend_schema(request=login_request, responses=login_response)
    @action(detail=False, methods=["post"])
    def login(self, request):
        payload = request.data
        email = payload.get("email")
        try:

            user = User.objects.get(email=email)
        except Exception as exc:
            print(exc)
            print("wrong email")
            return Response(
                    data={
                        "code": 5,
                        "status": False,
                        "data": {"message": "invalid Email or Password"},
                    },
                    status=401,
                )
        #compare password hash
        if not hashers.check_password(payload["password"], user.password):
            print("wrong password")
            return Response(
                data={
                    "code": 5,
                    "status": False,
                    "data": {"message": "invalid login credentials"},
                },
                status=401,
            )
        #check that password is not blacklisted
        if user.is_blacklisted is True:
            return Response(
                data={
                    "code": 5,
                    "status": False,
                    "data": {"message": "user is blacklisted, kindly contact admin"},
                },
                status=401,
            )
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        response = Response()
        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
        )
        response.set_cookie(
            key="accessToken",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
        )
        response.data = {"auth_credentials": access_token, "user": UserSerializer(user).data}
        response.status_code = 200
        return response
