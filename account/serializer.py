from rest_framework import serializers
from .models import User, Organisation, OrganisationUser

class UserSerializer(serializers.ModelSerializer):


    def update(self, instance, data):

        instance.save()
    
    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
            "email"
        )



class OrganisationSerializer(serializers.ModelSerializer):
    admin_id = serializers.SerializerMethodField()

    def get_admin_id(self, obj):
        return UserSerializer(obj.admin_id).data


    def update(self, instance, data):

        instance.save()
    
    class Meta:
        model = Organisation
        fields = (
            "id",
            "name",
            "num_of_staffs",
            "admin_id",
            "country",
            "state",
            "city",
            "address"
        )

class OrganisationSerializerPrivate(serializers.ModelSerializer):
    admin_id = serializers.SerializerMethodField()

    def get_admin_id(self, obj):
        return UserSerializer(obj.admin_id).data


    def update(self, instance, data):

        instance.save()
    
    class Meta:
        model = Organisation
        fields = (
            "id",
            "name",
            "staff_access_code",
            "num_of_staffs",
            "admin_id",
            "country",
            "state",
            "city",
            "address"
        )


class OrganisationUserSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data
    
    def get_organisation(self, obj):
        return OrganisationSerializer(obj.organisation).data


    def update(self, instance, data):

        instance.save()
    
    class Meta:
        model = OrganisationUser
        fields = (
            "organisation",
            "user",
            "role",
            "accepted"
        )