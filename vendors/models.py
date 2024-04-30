from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=100, help_text="Vendor's name.")
    contact_details = models.TextField(help_text="Contact information of the vendor.")
    address = models.TextField(help_text="Physical address of the vendor.")
    vendor_code = models.CharField(max_length=20, unique=True, help_text="A unique identifier for the vendor.")
    on_time_delivery_rate = models.FloatField(default=0.0, help_text="Tracks the percentage of on-time deliveries.")
    quality_rating_avg = models.FloatField(default=0.0, help_text="Average rating of quality based on purchase orders.")
    average_response_time = models.FloatField(default=0.0, help_text="Average time taken to acknowledge purchase orders.")
    fulfillment_rate = models.FloatField(default=0.0, help_text="Percentage of purchase orders fulfilled successfully.")

    def __str__(self) -> str:
        return self.name
