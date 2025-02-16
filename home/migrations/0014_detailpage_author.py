# Generated by Django 5.1.6 on 2025-02-16 13:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
        ("home", "0013_rename_cta_sub_title_homepage_cta_subtitle"),
    ]

    operations = [
        migrations.AddField(
            model_name="detailpage",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="detail_pages",
                to="base.author",
            ),
        ),
    ]
