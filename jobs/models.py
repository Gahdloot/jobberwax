from django.db import models
from account.models import User, Organisation, OrganisationUser
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Job(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    fields = models.JSONField(default={})
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)
    #add json for questions


class Application(models.Model):
    class Status(models.TextChoices):
        UnderReview = "UnderReview", _("UnderReview")
        Rejected = "Rejected", _("Rejected")
        Accepted = "Accepted", _("Accepted")
        Employed = "Employed", _("Employed")

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    additional_data = models.JSONField(default={})
    resume = models.CharField(max_length=250, null=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
    status = models.TextField(choices=Status.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True)
