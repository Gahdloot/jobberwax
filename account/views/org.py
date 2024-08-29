import logging

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from account.models import Organisation, OrganisationUser
from account.serializer import OrganisationSerializer, OrganisationUserSerializer, OrganisationSerializerPrivate
from account.authenticate import APIAuthentication
from secrets import token_urlsafe


class OrganisationViewset(ViewSet):
    authentication_classes = [APIAuthentication]

    @action(detail=False, methods=['post'], url_path='create')
    def custom_create(self, request):
        payload = request.data
        required_field = ["name", "city", "state", "country"]
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

            org = Organisation(
                name=payload.get("name"),
                city=payload.get("city"),
                state=payload.get("state"),
                country=payload.get("country"),
                admin_id=request.user,
                staff_access_code=token_urlsafe(5)
            )
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
        
    @action(detail=True, methods=["post"])
    def accept(self, request, pk):
        uid = request.GET.get("user", "123")
        payload = request.data
        try:
            org = Organisation.objects.get(id=pk)
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
            org.role = payload["role"]
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