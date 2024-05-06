import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.core.validators import MinValueValidator


class Vendor(models.Model):

    name = models.CharField(max_length=200)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=120, default=uuid.uuid4, unique=True, blank=True)
    on_time_delivery_rate = models.FloatField(validators=[MinValueValidator(0.00)], default=0.00)
    quality_rating_avg = models.FloatField(validators=[MinValueValidator(0.00)], default=0.00)
    average_response_time = models.FloatField(validators=[MinValueValidator(0.00)], default=0.00)
    fulfillment_rate = models.FloatField(validators=[MinValueValidator(0.00)], default=0.00)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):

        return str(self.name)


PURCHASE_STATUS = {
    "Pending": "Pending",
    "Completed": "Completed",
    "Cancelled": "Cancelled"
}


class PurchaseOrder(models.Model):

    po_number = models.CharField(max_length=120, default=uuid.uuid4, unique=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.CharField(max_length=30, choices=PURCHASE_STATUS, default="pending")
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        if not self.delivery_date:
            self.delivery_date = timezone.now() + timedelta(days=(int(self.quantity))//5 + 1)
        super().save(*args, **kwargs)
