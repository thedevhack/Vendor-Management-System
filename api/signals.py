from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from .models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    """
    On time delivery rate is calculated on basis of that the time
    at which status is changed to completed at that time delivery date
    is set, and we calculate what should have been the expected delivery
    date according to number of items it is 1 day greater than number of items
    divided by 5 (i.e. in 1day we can deliver 5 items and 1day for slack)
    and then we use filter to get all orders where delivery date was less
    than or equal to our expected delivery date divided by total completed
    orders
    :param sender:
    :param instance:
    :param kwargs:
    :return None:
    """

    if instance.status == "Completed":
        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status="Completed")
        total_completed_orders_count = total_completed_orders.count()
        issue_date = instance.issue_date
        if timezone.is_naive(issue_date):
            issue_date = timezone.make_aware(issue_date)

        expected_delivery_date = issue_date + timedelta(days=(int(instance.quantity))//5 + 1)
        ontime_completed_orders = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            status='Completed',
            delivery_date__lte=expected_delivery_date
        )
        ontime_completed_orders_count = ontime_completed_orders.count()
        ontime_delivery_rate = ontime_completed_orders_count / total_completed_orders_count
        instance.vendor.on_time_delivery_rate = float(ontime_delivery_rate)
        instance.vendor.save()


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, **kwargs):
    """
    quality rating average is average of all ratings given to vendor
    for the purchase orders excluding orders where no rating was given
    :param sender:
    :param instance:
    :param kwargs:
    :return None:
    """

    if instance.status == "Completed" and instance.quality_rating is not None:
        vendor = instance.vendor
        avg_rating = PurchaseOrder.objects.filter(vendor=vendor,
                                                  status='Completed',
                                                  quality_rating__isnull=False
                                                  ).aggregate(
            Avg('quality_rating'))['quality_rating__avg']
        vendor.quality_rating_avg = float(avg_rating)
        vendor.save()


@receiver(post_save, sender=PurchaseOrder)
@receiver(post_delete, sender=PurchaseOrder)
def update_fulfillment_ratio(sender, instance=None, **kwargs):
    """
    it is the ratio of how many orders were completed successfully to the
    total number of orders
    :param sender:
    :param instance:
    :param kwargs:
    :return:
    """
    total_po_count = PurchaseOrder.objects.filter(
        vendor=instance.vendor).count()
    fulfilled_po_count = PurchaseOrder.objects.filter(
        vendor=instance.vendor, status='Completed').count()

    if total_po_count > 0:
        fulfillment_ratio = fulfilled_po_count / total_po_count
    else:
        fulfillment_ratio = 0

    instance.vendor.fulfillment_rate = float(fulfillment_ratio)
    instance.vendor.save()
