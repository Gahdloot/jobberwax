from rest_framework import serializers
from .models import Job, Application
from account.serializer import UserSerializer, OrganisationSerializer

class JobSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        return UserSerializer(obj.created_by).data
    

    def get_organisation(self, obj):
        return OrganisationSerializer(obj.organisation).data


    def update(self, instance, data):
        
        instance.save()
    
    class Meta:
        model = Job
        fields = (
            "id",
            "created_by",
            "organisation",
            "title",
            "description",
            "fields",
            "created_at",
            "modified_at",
            "active"
        )

class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data
    


    def update(self, instance, data):
        instance.status = data.get("status", instance.status)
        instance.save()
    
    class Meta:
        model = Job
        fields = (
            "id",
            "user",
            "additional_data",
            "resume",
            "created_at",
            "modified_at",
            "status",
            "created_at",
            "modified_at"
        )