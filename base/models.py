from django.db import models
from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm

# Create your models here.
class CustomPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].help_text = "The page title as you'd like it to be seen by the public. The title's length is limited to 60 characters"
        self.fields['seo_title'].required = True
        self.fields['search_description'].required = True

        def clean(self):
            """Validate the form fields."""
            cleaned_data = super().clean()
            
            errors = {}
            
            if len(cleaned_data.get('title', '')) > 60:
                errors['title'] = "The title's length is limited to 60 characters"
            if not cleaned_data.get('seo_title'):
                errors['seo_title'] = "You must provide a SEO title"
            if not cleaned_data.get('search_description'):
                errors['search_description'] = "You must provide a meta description"
            
            if errors:
                raise ValidationError(errors)
                
            return cleaned_data