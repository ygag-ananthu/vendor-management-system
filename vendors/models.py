from django.db import models
from django.utils import timezone
from django.db.models import Avg, F
from django.db.models import Sum

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

    def on_time_delivery_calculator(self,completed_orders):
        total_completed_orders = completed_orders.count()
        #at this moment timezone.now is the delivered date
        if total_completed_orders > 0:
            on_time_delivered_orders = completed_orders.filter(delivery_date__gte=timezone.now())
            on_time_delivery_rate = (on_time_delivered_orders.count() / total_completed_orders) * 100
            self.on_time_delivery_rate = on_time_delivery_rate
        else:
            self.on_time_delivery_rate = 0
        self.save()

    def quality_rating_avg_calculator(self,completed_orders):
        quality_rated_order = completed_orders.filter(quality_rating__isnull = False)
        total_quality_rated_order = quality_rated_order.count()
        if total_quality_rated_order > 0:
            quality_rating_sum = quality_rated_order.aggregate(Sum('quality_rating'))['quality_rating__sum']
            self.quality_rating_avg = quality_rating_sum / total_quality_rated_order
        else:
            self.quality_rating_avg = 0
        self.save()
            
    def average_response_time_calculator(self):
        acknowledged_orders = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)

        average_response_time_timedelta = acknowledged_orders.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time']

        if average_response_time_timedelta is not None:
            average_response_time_seconds = average_response_time_timedelta.total_seconds()
            self.average_response_time = average_response_time_seconds
        else:
            self.average_response_time = 0

        self.save()

            
    def fulfillment_rate_calculator(self):
        successful_orders = self.purchaseorder_set.filter(status='completed', issue_date__isnull=False)
        total_orders = self.purchaseorder_set.exclude(status='canceled').count()
        fulfillment_rate = successful_orders.count() / total_orders * 100 if total_orders > 0 else 0
        self.fulfillment_rate = fulfillment_rate
        self.save()
        