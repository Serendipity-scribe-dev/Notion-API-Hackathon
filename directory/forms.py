from django import forms
from .models import MemberProfile,NotionConfig

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['name', 'bio', 'skills', 'availability', 'location', 'links']
        #fields = '__all__'

class NotionConfigForm(forms.ModelForm):
    class Meta:
        model = NotionConfig
        fields = ['api_key', 'database_id']