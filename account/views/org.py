from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from account.models import Organisation, OrganisationUser
from account.serializer import OrganisationSerializer, OrganisationUserSerializer, OrganisationSerializerPrivate
from account.authenticate import APIAuthentication
from secrets import token_urlsafe
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from swagger.api_request import (
    org_request,
    test_response,
    join_org_request,
    accept_invite_params
)

class OrganisationViewset(ViewSet):
    authentication_classes = [APIAuthentication]

    #create organisation
    @swagger_auto_schema(method='post', request_body=org_request, responses=test_response)
    @action(detail=False, methods=['post'], url_path='create')
    def custom_create(self, request):
        payload = request.data
        required_field = ["name", "city", "state", "country"]
        #check that fields are not blank
        for field in required_field:
            if payload.get(field) is None or len(payload.get(field)) < 3 or isinstance(field, str) is False:
                return Response(
                data={
                    "code": 5,
                    "status": False,
                    "data": {"message": f"Invalid {field} field"},
                },
                status=400,
            )
        try:
            #run transaction on both tables
            with transaction.atomic():
                org = Organisation(
                    name=payload.get("name"),
                    city=payload.get("city"),
                    state=payload.get("state"),
                    country=payload.get("country"),
                    admin_id=request.user,
                    staff_access_code=token_urlsafe(2)
                )
                if isinstance(payload.get("valuation"), int) is True:
                    org.valuation = abs(payload.get("valuation"))
                org.save()


                
                org_user = OrganisationUser(
                    organisation=org,
                    user=request.user,
                    accepted=True,
                    role="ORG_ADMIN"
                )
                org_user.save()
                return Response(
                        data={
                            "status": True,
                            "data": {"organisation": OrganisationSerializer(org).data},
                        },
                        status=200,
                    )
        except Exception as exc:
            return Response(
                    data={
                        "code": 4,
                        "status": False,
                        "data": {"message": f"{exc}"},
                    },
                    status=400,
                )
        
    def retrieve(self, request, pk):
        try:
            #retrive organisation id, if the request is made by an admin, staff access code will be revealed
            org = Organisation.objects.get(id=pk)
            if org.admin_id == request.user:
                post_data = OrganisationSerializerPrivate(org).data
            else:
                post_data = OrganisationSerializer(org).data
            return Response(data={"code": 0, "data": post_data})
        except Exception:
            return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "Cannot find organisation"},
                    },
                    status=404,
                )
        
    
    @swagger_auto_schema(method='post', request_body=join_org_request, responses=test_response)
    @action(detail=True, methods=['post'], url_path='staff/join')
    def join(self, request, pk):
        payload = request.data

        try:
            org = Organisation.objects.get(id=pk)
            if org.staff_access_code == payload.get("access_code"):
                if OrganisationUser.objects.filter(organisation=org, user=request.user).exists():
                    return Response(
                        data={
                            "status": False,
                            "data": {"message": "User already Exists in organisation"},
                        },
                        status=400,
                    )
                org_user = OrganisationUser(
                organisation=org,
                user=request.user,
                role="UNASSIGNED",
                )
                org_user.save()
                return Response(
                        data={
                            "status": True,
                            "data": {"message": "Added to organisation"},
                        },
                        status=200,
                    )
            return Response(
                        data={
                            "status": False,
                            "data": {"message": "Invalid Code Access Code"},
                        },
                        status=400,
                    )
        except Exception as exe:
            print(exe)
            return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "Cannot find organisation"},
                    },
                    status=404,
                )
    
    # @swagger_auto_schema(method='post', manual_parameters=accept_invite_params)
    @action(detail=True, methods=["post"])
    def accept(self, request, pk):
        uid = request.GET.get("user", "123")
        payload = request.data
        try:
            org = Organisation.objects.get(id=pk)
            if payload.get("role") not in ["ORG_STAFF", "ORG_HR"]:
                return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "role can be either be ORG_STAFF or ORG_HR"},
                    },
                    status=400,
                )
            if org.admin_id != request.user:
                return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "Only Organisation Owner Can accept member"},
                    },
                    status=403,
                )
            if OrganisationUser.objects.filter(id=uid).exists() is False:
                return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "cannot Get User"},
                    },
                    status=404,
                )
            org_user = OrganisationUser.objects.get(id=uid)
            org_user.accepted = True
            org_user.role = payload["role"]
            org_user.save()
            org.save()
            return Response(
                    data={
                        "status": True,
                        "data": {"message": "Added user to organisation"},
                    },
                    status=200,
                )
        except Exception as exc:
            print(exc)
            return Response(
                    data={
                        "code": 1,
                        "status": False,
                        "data": {"message": "cannot Get organisation"},
                    },
                    status=404,
                )
        
    def list(self, request):
        org_users = OrganisationUser.objects.filter(user=request.user)
        serializer = OrganisationUserSerializer(org_users, many=True).data
        return Response(
                    data={
                        "status": True,
                        "data": {"Organisations": serializer},
                    },
                    status=200,
                )
    

class OrganisationUserViewset(ViewSet):
    authentication_classes = [APIAuthentication]

    #For getting all Users
    @action(detail=True, methods=["get"])
    def all(self, request, pk):
        org_users = OrganisationUser.objects.filter(organisation=pk)
        serializer = OrganisationUserSerializer(org_users, many=True).data
        return Response(
                    data={
                        "status": True,
                        "data": {"Organisations": serializer},
                    },
                    status=200,
                )
    
    
        
        
        