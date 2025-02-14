from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.images.models import Image, AbstractImage, AbstractRendition
from wagtail.admin.panels import FieldPanel
from wagtail.images import get_image_model
from django.core.exceptions import ValidationError
from wagtail.admin.forms import WagtailAdminPageForm
from base.models import CustomPageForm



class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + ('caption',)

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body=RichTextField(blank=True, null=True)
    image=models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    cta_url=models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        FieldPanel("subtitle"),
        FieldPanel("cta_url"),
        FieldPanel("body"),
        FieldPanel("image"),
    ]

class IndexPage(Page):
    ## Page Attributes
    template = "home/index_page.html"
    page_description = "#HELP_TEXT... Index page for listing blog entries"
    max_count = 1
    parent_page_types = ['home.HomePage']
    subpage_types = ['home.DetailPage'] # empty list means no subpages allowed 
    base_form_class = CustomPageForm # help text and settings for the base Page fields from Wagtail (brought from base/models.py)

    ## Page Fields
    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True, features=['h2', 'h3', 'bold', 'italic', 'ol', 'ul', 'link'])
    cta_url=models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    ## Page Panels
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('cta_url'),
        FieldPanel('body'),
    ]

    ## Page Context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # Add extra variables and return the updated context
        context['child_pages'] = IndexPage.objects.child_of(self).live() # get all child pages
        context["page_description"] = self.page_description
        context['context_var'] = "This is a context variable"
        return context
    
    ## Page Validations
    def clean(self):
        super().clean()

        errors={}

        if len(self.subtitle)>60 or len(self.subtitle)<10:
            errors['subtitle']="The subtitle's length is limited to 10-60 characters "
           
        if errors:
            raise ValidationError(errors)

    ## Page Meta  
    class Meta:
        verbose_name = "Index page"



### Detail Page and Tags

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase


class BlogPageTags(TaggedItemBase):
    content_object = ParentalKey(
        'home.DetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

class DetailPage(Page):
    template = "home/detail_page.html"
    page_description = "Detail page for blog entries"
    parent_page_types = ['home.IndexPage']

    subtitle = models.CharField(max_length=100, blank=True)
    body = RichTextField(blank=True)
    tags=ClusterTaggableManager(through=BlogPageTags, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        FieldPanel('tags'),
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "Detail page"



