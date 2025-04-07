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

def get_dynamic_profile_form(schema):
     
    class DynamicProfileForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field_name, field_type in schema.items():
                is_required = True if field_name.lower() == ["name","date"] else False  # ✅ Only Name is required

                # Generate generic placeholder
                base_placeholder = f"Enter {field_name}"

                # Type-specific tweaks
                if field_type == "multi_select":
                    placeholder = f"Comma-separated values for {field_name}"
                elif field_type == "date":
                    placeholder = f"Pick a date"
                elif field_type in ["select", "status"]:
                    placeholder = f"Type or pick {field_name.lower()}"
                elif field_type == "url":
                    placeholder = f"https://example.com"
                elif field_type == "email":
                    placeholder = f"you@example.com"
                elif field_type == "phone_number":
                    placeholder = f"+1234567890"
                else:
                    placeholder = base_placeholder
        
                # Title & Text Fields
                if field_type in ["title", "rich_text", "text"]:
                    self.fields[field_name] = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={'class': 'form-control',
                        'placeholder': placeholder,
                        'rows': 3,  # You can increase this number for more height
                        })
                        
                    )

                # Multi-Select (Comma-separated input)
                elif field_type == "multi_select":
                    self.fields[field_name] = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': placeholder}),
                        #help_text="Comma-separated values"
                    )

                # Select or Status
                elif field_type in ["select", "status"]:
                    self.fields[field_name] = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': placeholder})
                    )

                # Date Picker
                elif field_type == "date":
                    self.fields[field_name] = forms.DateField(
                        label=field_name,
                        required=is_required,
                        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control','placeholder': placeholder})
                    )

                # Email
                elif field_type == "email":
                    self.fields[field_name] = forms.EmailField(
                        label=field_name,
                        required=is_required,
                        widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': placeholder})
                    )

                # Phone
                elif field_type == "phone_number":
                    self.fields[field_name] = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={'type': 'tel', 'class': 'form-control','placeholder': placeholder})
                    )

                # URL
                elif field_type == "url":
                    self.fields[field_name] = forms.URLField(
                        label=field_name,
                        required=is_required,
                        widget=forms.URLInput(attrs={'class': 'form-control','placeholder': placeholder})
                    )

                # Checkbox
                elif field_type == "checkbox":
                    self.fields[field_name] = forms.BooleanField(
                        label=field_name,
                        required=False  # Checkboxes should always be optional unless otherwise needed
                    )

                # Fallback for anything else
                else:
                    self.fields[field_name] = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': placeholder})
                    )

    return DynamicProfileForm