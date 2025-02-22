from django.db import models

from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm
from django.contrib.contenttypes.fields import GenericRelation
from wagtail.models import RevisionMixin, LockableMixin, DraftStateMixin, TranslatableMixin, PreviewableMixin
from wagtail.admin.panels import FieldPanel, PublishingPanel
from wagtail.search import index

from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import TaggedItemBase, Tag


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

@register_snippet
class Author(
        TranslatableMixin,
        PreviewableMixin,  # Allows previews
        LockableMixin,  # Makes the model lockable
        DraftStateMixin,  # Needed for Drafts
        RevisionMixin,  # Needed for Revisions
        index.Indexed,  # Makes this searchable; don't forget to run python manage.py update_index
        models.Model
    ):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    revisions = GenericRelation("wagtailcore.Revision", related_query_name="author")

    panels = [
        FieldPanel("name", permission="blogpages.can_edit_author_name"),
        FieldPanel("bio"),
        PublishingPanel(),
    ]

    #might need to do `python manage.py update_index` after adding this
    search_fields = [
        index.FilterField('name'),
        index.SearchField('name'),
        index.AutocompleteField('name'),
    ]

    def __str__(self):
        return self.name

    @property
    def preview_modes(self):
        return PreviewableMixin.DEFAULT_PREVIEW_MODES + [
            ("dark_mode", "Dark Mode")
        ]

    def get_preview_template(self, request, mode_name):
        # return "includes/author.html"  # Default for a single preview template
        templates = {
            "": "snippets/author.html", # Default
            "dark_mode": "snippets/author_dark_mode.html"
        }
        return templates.get(mode_name, templates[""])

    def get_preview_context(self, request, mode_name):
        context = super().get_preview_context(request, mode_name)
        context['warning'] = "This is a preview"
        return context

