# Generated by Django 5.1.6 on 2025-02-19 03:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listing_of_watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
