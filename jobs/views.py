from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from account.models import Organisation, OrganisationUser
from jobs.models import Job, Application
from jobs.serializers import JobSerializer, ApplicationSerializer, OrganisationSerializer
from account.authenticate import APIAuthentication
from secrets import token_urlsafe
# Create your views here.

class PublicJobViewsets(ViewSet):
    authentication_classes = []

    def retrieve(self, request, pk):
        try:
            jobs = Job.objects.get(id=pk)
            serializer = JobSerializer(jobs).data
            return Response(
                    data={
                        "status": "success",
                        "data": {"jobs": serializer},
                    },
                    status=200,
                )
        except Exception as Exc:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
                        "data": {"message": "Cannot get Job"},
                    },
                    status=400,
                )


    def list(self, request):
        try:
            jobs = Job.objects.filter(active=True)
            serializer = JobSerializer(jobs, many=True).data
            return Response(
                    data={
                        "status": "success",
                        "data": {"jobs": serializer},
                    },
                    status=200,
                )
        except Exception as Exc:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
                        "data": {"message": f"{Exc}"},
                    },
                    status=400,
                )


class JobViewset(ViewSet):
    authentication_classes = [APIAuthentication]

    def create(self, request):
        payload = request.data
        required_field = ["title", "description", "organisation"]
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
            org = Organisation.objects.get(id=payload.get("organisation"))

        except:
            return Response(
                data={
                    "code": 5,
                    "status": "fail",
                    "data": {"message": "Organisation does not Exists"},
                },
                status=404,
            )

        try:
            if isinstance(payload.get("fields"), dict) is False:
                return Response(
                data={
                    "code": 5,
                    "status": "fail",
                    "data": {"message": "Expected a dictionary '{}' on field"},
                },
                status=404,
            )
            job = Job(
                created_by=request.user,
                organisation=org,
                title=payload.get("title"),
                description=payload.get("description"),
                active=payload.get("active", True),
                fields=payload.get("fields")
            )
            job.save()
            return Response(
                    data={
                        "status": "success",
                        "data": {"jobs": JobSerializer(job).data}
                    },
                    status=200,
                )
        except Exception as e:
            return Response(
                data={
                    "code": 4,
                    "status": "fail",
                    "data": {"message": f"{e}"},
                },
                status=400,
            )
        
    @action(detail=True, methods=["get"])
    def organisation(self, request, pk):
        try:
            org = Organisation.objects.get(id=pk)
        except Exception:
            return Response(
                    data={
                        "code": 1,
                        "status": "fail",
                        "data": {"message": "Cannot find organisation"},
                    },
                    status=404,
                )
        try:
            jobs = Job.objects.filter(organisation=org)
            serializer = JobSerializer(jobs, many=True).data
            return Response(
                    data={
                        "status": "success",
                        "data": {"jobs": serializer},
                    },
                    status=200,
                )
        except Exception as Exc:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
                        "data": {"message": f"{Exc}"},
                    },
                    status=400,
                )
        
    def update(self, request, pk):
        payload = request.data
        try:
            job = Job.objects.get(id=pk)
            serializer = JobSerializer(job, payload, partial=True)
            #update endpoint here
            return Response(
                    data={
                        "status": "success",
                        "data": {"jobs": serializer},
                    },
                    status=200,
                )
        except Exception as Exc:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
                        "data": {"message": "Cannot get Job"},
                    },
                    status=404,
                )
        

class ApplicationViewset(ViewSet):
    authentication_classes = [APIAuthentication]

    def create(self, request):
        payload = request.data

        try:
            if Organisation.objects.filter(id=payload.get("organisation")).exists() is True:
                return Response(
                    data={
                        "status": "fail",
                        "data": {"message": "Cannot get Organisation"},
                    },
                    status=404,
                )
            application = Application(
                user=request.user,
                resume=payload.get("resume"),
                additional_data=payload.get("additional_data", {}),
                status="UnderReview"
            )
            application.save()
            return Response(
                    data={
                        "status": "success",
                        "data": {"message": "Application Sent"},
                    },
                    status=201,
                )
        except Exception as exe:
            return Response(
                    data={
                        "code": 4,
                        "status": "fail",
                        "data": {"message": f"{exe}"},
                    },
                    status=400,
                )
        

    def list(self, request):
        job_id = request.query_params.get("job")
        if job_id is None:
            return Response(
                    data={
                        "status": False,
                        "data": {"message": "job in params"},
                    },
                    status=400)
        else:
            try:
                job = Job.objects.get(id=job_id) 
                applicants = Application.objects.filter(job=job)
                serializer = ApplicationSerializer(applicants, many=True).data
                return Response(
                    data={
                        "status": True,
                        "data": {"jobs": serializer},
                    },
                    status=200)
            except Exception as exe:
                return Response(
                    data={
                        "status": False,
                        "data": {"message": str(exe)},
                    },
                    status=200)