from django.db import models

from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm

# Custom Page For that can be used in any Page class
# base_form_class = CustomPageForm # help text and settings for the base Page fields from Wagtail (brought from base/models.py)
class CustomPageForm(WagtailAdminPageForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

         # Remove show_in_menus field
        self.fields.pop('show_in_menus', None)

        # Existing field customizations
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
        

# Snippet
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import TaggedItemBase, Tag

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 400
    list_display = ["name","slug"]
    search_fields = ["name"]
    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]
