import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Vendor, PurchaseOrder


class VendorPerformanceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'token {self.token}')
        self.vendor = Vendor.objects.create(name="Test Vendor", contact_details="Test Contact", address="Test Address")
        self.po = PurchaseOrder.objects.create(vendor=self.vendor,
                                               items={"thing": "something"},
                                               quantity=11, status="Pending")

    def test_add_new_pos_and_make_some_complete(self):
        for _ in range(4):
            PurchaseOrder.objects.create(vendor=self.vendor,
                                         items={"thing": "something"},
                                         quantity=11,
                                         status="Pending")
        time.sleep(1)
        acknowledge_url = reverse('po_acknowledge', kwargs={'id': 2})
        self.client.post(acknowledge_url)
        acknowledge_url = reverse('po_acknowledge', kwargs={'id': 3})
        self.client.post(acknowledge_url)
        complete_task = reverse('po_detail', kwargs={'id': 2})
        self.client.put(complete_task, data={"vendor": self.vendor.id,
                                             "items": {"thing": "something"},
                                             "quantity": 11,
                                             'status': 'Completed',
                                             'quality_rating': 7}, format='json')
        self.po = PurchaseOrder.objects.get(id=2)
        response = self.client.get(reverse('po_detail', kwargs={'id': 2}))
        print("on_time_delivery_rate -> ", Vendor.objects.get(id=response.data['vendor']).on_time_delivery_rate)
        print("quality_rating_avg -> ", Vendor.objects.get(id=response.data['vendor']).quality_rating_avg)
        print("average_response_time -> ", Vendor.objects.get(id=response.data['vendor']).average_response_time)
        print("fulfillment_rate -> ", Vendor.objects.get(id=response.data['vendor']).fulfillment_rate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['status'] == "Completed")

    def test_acknowledge_endpoint(self):
        url = reverse('po_acknowledge', kwargs={'id': self.po.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.po.refresh_from_db()
        self.assertIsNotNone(self.po.acknowledgment_date)
        self.assertIsNotNone(self.vendor.average_response_time)
