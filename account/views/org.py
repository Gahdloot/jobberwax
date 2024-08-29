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

    def create(self, request):
        payload = request.data
        required_field = ["name", "city", "state", "country"]
        for field in required_field:
            if payload.get(field) is None or len(payload.get(field)) < 3 or isinstance(payload.get("email"), str) is False:
                return Response(
                data={
                    "code": 5,
                    "status": "fail",
                    "data": {"message": f"Invalid {field} field"},
                },
                status=401,
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
                        "status": "success",
                        "data": {"organisation": OrganisationSerializer(org).data},
                    },
                    status=200,
                )
        except Exception as exc:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
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
                        "status": "fail",
                        "data": {"message": "Cannot find organisation"},
                    },
                    status=404,
                )
        

    @action(detail=True, methods=["post"])
    def join(self, request, pk):
        payload = request.data
        try:
            org = Organisation.objects.get(id=pk)
            if org.staff_access_code == payload.get("access_code"):
                org_user = OrganisationUser(
                organisation=org,
                user=request.user,
                role="UNASSIGNED",
            )
            org_user.save()
            return Response(
                    data={
                        "status": "success",
                        "data": {"message": "Added to organisation"},
                    },
                    status=200,
                )
        except Exception:
            return Response(
                    data={
                        "code": 1,
                        "status": "fail",
                        "data": {"message": "Cannot find organisation"},
                    },
                    status=404,
                )
        
    @action(detail=True, methods=["post"])
    def accept(self, request, pk, uid):
        payload = request.data
        try:
            org = Organisation.objects.get(id=pk)
            if org.admin_id != request.user:
                return Response(
                    data={
                        "code": 1,
                        "status": "fail",
                        "data": {"message": "Only Organisation Owner Can accept member"},
                    },
                    status=403,
                )
            org_user = OrganisationUser.objects.get(id=uid)
            org_user.accepted = True
            org.role = payload["role"]
            org.save()
            return Response(
                    data={
                        "status": "success",
                        "data": {"message": "Added user to organisation"},
                    },
                    status=200,
                )
        except Exception as exc:
            return Response(
                    data={
                        "code": 1,
                        "status": "fail",
                        "data": {"message": f"{exc}"},
                    },
                    status=404,
                )
        
    def list(self, request):
        org_users = OrganisationUser.objects.filter(user=request.user)
        serializer = OrganisationUserSerializer(org_users, many=True).data
        return Response(
                    data={
                        "status": "success",
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
                        "status": "success",
                        "data": {"Organisations": serializer},
                    },
                    status=200,
                )