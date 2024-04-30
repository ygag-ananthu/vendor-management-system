from django.db import models
from vendors.models import Vendor

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Date of the performance record.")
    on_time_delivery_rate = models.FloatField(help_text="Historical record of the on-time delivery rate.")
    quality_rating_avg = models.FloatField(help_text="Historical record of the quality rating average.")
    average_response_time = models.FloatField(help_text="Historical record of the average response time.")
    fulfillment_rate = models.FloatField(help_text="Historical record of the fulfilment rate.")

    def __str__(self) -> str:
        return f'Performance for {self.vendor} on {self.date}'
