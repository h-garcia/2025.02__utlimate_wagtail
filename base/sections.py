# base/sections.py

from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PageChooserPanel,
)

class cta_section(models.Model):
    """Call to Action section.
    Add the template to the page where this sexction will be used.
    """
    
    cta_title = models.CharField(max_length=100, blank=False, null=True) 
    cta_subtitle = models.TextField(max_length=255, blank=False, null=True)
    cta_primary_text = models.CharField(max_length=50, blank=False, null=True)
    cta_primary_url = models.ForeignKey(
        "wagtailcore.Page",
        blank=False,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )


    panels = [
        MultiFieldPanel(
            [
            FieldPanel("cta_title"),
            FieldPanel("cta_subtitle"),
            FieldPanel("cta_primary_text"),
            PageChooserPanel("cta_primary_url"),
            ],
            heading="Section: CTA",
            help_text="This section is used to create a call to action section.",
        )
    ]

    class Meta:
        abstract = True


