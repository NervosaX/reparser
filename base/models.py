from django.db import models


class Detail(models.Model):

    DETAIL_CHOICE = (
        ('S', 'Scheduled to view'),
        ('D', 'Definitely like'),
        ('U', 'Not Checked'),
        ('P', 'Possible'),
        ('N', 'NO.')
    )

    status = models.CharField(max_length=1, choices=DETAIL_CHOICE, default='U')

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
    crow_fly_distance = models.FloatField(
        blank=True,
        null=True
        )

    cable_length = models.FloatField(
        blank=True,
        null=True
        )

    estimated_speed = models.FloatField(
        blank=True,
        null=True
        )

    # Travel to Oakleigh
    oak_summary = models.CharField(
        max_length=100,
        blank=True,
        null=True
        )

    def get_nearest_railway(self):
        if (self.railwayposition_set.count()):
            return min(self.railwayposition_set.all(), key=lambda i: i.distance)
        else:
            return None

    
class RailwayPosition(models.Model):

    detail = models.ForeignKey(Detail)

    # Railway line name
    line_name = models.CharField(
        max_length=100,
        blank=True
        )

    # Distance from address to railway line
    distance = models.FloatField(blank=True)