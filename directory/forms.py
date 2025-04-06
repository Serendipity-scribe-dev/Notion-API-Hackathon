from django import forms
from .models import MemberProfile

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        #fields = ['name', 'bio', 'skills', 'availability', 'location', 'links']
        fields = '__all__'
