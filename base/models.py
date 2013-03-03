from django.db import models

class Detail(models.Model):

    # Basic details
    address = models.CharField(
        unique=True,
        max_length=300
    )

    title = models.CharField(
        max_length=300,
        blank=True
        )    

    price = models.CharField(
        max_length=300,
        blank=True
        )

    url = models.CharField(
        max_length=500,
        )

    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    carspaces = models.IntegerField(default=0)

    # PT Melb details
    pt_depart_time = models.CharField(
        max_length=100,
        blank=True
        )

    pt_arrive_time = models.CharField(
        max_length=100,
        blank=True
        )

    pt_duration = models.CharField(
        max_length=100,
        blank=True
        )

    # ADSL2 details
    crow_fly_distance = models.CharField(
        max_length=100,
        blank=True
        )

    cable_length = models.CharField(
        max_length=100,
        blank=True
        )

    estimated_speed = models.CharField(
        max_length=100,
        blank=True
        )

    
class RailwayPosition(models.Model):

    detail = models.ForeignKey(Detail)

    # Railway line name
    line_name = models.CharField(
        max_length=100,
        blank=True
        )

    # Distance from address to railway line
    distance = models.CharField(
        max_length=100,
        blank=True
        )