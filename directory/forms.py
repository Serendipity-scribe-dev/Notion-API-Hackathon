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

            for field_name, field_info in schema.items():
                if isinstance(field_info, str):
                    field_info = {"type": field_info}

                field_type = field_info.get("type")
                options = field_info.get("options", [])
                is_required = field_name.lower() in ["name", "date"]

                # Generate generic placeholder
                base_placeholder = f"Enter {field_name}"

                # Type-specific tweaks
                if field_type == "multi_select":
                    placeholder = f"Select one or more options"
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
                    field = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': placeholder,
                            'autocomplete': 'on',
                        })
                    )

                # Multi-Select Checkboxes
                elif field_type == "multi_select" and options:
                    field = forms.MultipleChoiceField(
                        label=field_name,
                        required=is_required,
                        choices=[(opt, opt) for opt in options],
                        widget=forms.CheckboxSelectMultiple(attrs={
                            'class': 'form-check-input',
                            'placeholder': placeholder,
                        }),
                    )

                # Select Dropdown
                elif field_type == "select" and options:
                    field = forms.ChoiceField(
                        label=field_name,
                        choices=[('', 'Select an option')] + [(opt, opt) for opt in options],
                        required=is_required,
                        widget=forms.Select(attrs={
                            'class': 'form-select',
                            'placeholder': placeholder,
                        })
                    )

                # Date Picker
                elif field_type == "date":
                    field = forms.DateField(
                        label=field_name,
                        required=is_required,
                        widget=forms.DateInput(attrs={
                            'type': 'date',
                            'class': 'form-control',
                            'placeholder': placeholder
                        })
                    )

                # Email
                elif field_type == "email":
                    field = forms.EmailField(
                        label=field_name,
                        required=is_required,
                        widget=forms.EmailInput(attrs={
                            'class': 'form-control',
                            'placeholder': placeholder
                        })
                    )

                # Phone
                elif field_type == "phone_number":
                    field = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={
                            'type': 'tel',
                            'class': 'form-control',
                            'placeholder': placeholder
                        })
                    )

                # URL
                elif field_type == "url":
                    field = forms.URLField(
                        label=field_name,
                        required=is_required,
                        widget=forms.URLInput(attrs={
                            'class': 'form-control',
                            'placeholder': placeholder
                        })
                    )

                # Checkbox (Boolean)
                elif field_type == "checkbox":
                    field = forms.BooleanField(
                        label=field_name,
                        required=False
                    )

                # Fallback
                else:
                    field = forms.CharField(
                        label=field_name,
                        required=is_required,
                        widget=forms.TextInput(attrs={
                            'class': 'form-control',
                            'placeholder': placeholder
                        })
                    )

                # 👉 Tag widget type for template use
                field.widget.widget_type = field_type

                # Add field to form
                self.fields[field_name] = field

    return DynamicProfileForm
