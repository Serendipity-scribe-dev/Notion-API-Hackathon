from django.db import models
from django.apps import apps

class MemberProfile(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    skills = models.CharField(max_length=300)  # Comma-separated
    availability = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    notion_page_id = models.CharField(max_length=255, blank=True, null=True) #

    def __str__(self):
        return self.name

class NotionConfig(models.Model):
    api_key = models.CharField(max_length=255)
    database_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Notion Configuration"

class DynamicProfile(models.Model):
    data = models.JSONField()  # holds all the dynamic field data
    notion_page_id = models.CharField(max_length=255, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.data.get("Name", "Unnamed Profile")

def get_dynamic_model():
    return apps.get_model('directory', 'DynamicProfile')