from django.urls import path
from .views import (CreateListVendorAPIView,
                    RetrieveUpdateDeleteVendorAPIView,
                    CreateListPurchaseAPIView,
                    RetrieveUpdateDeletePurchaseAPIView,
                    VendorPerformanceRetrieveAPIView,
                    AcknowledgeAPIView)

urlpatterns = [
    path("vendors/", CreateListVendorAPIView.as_view(), name="vendors_get"),
    path("vendors/<int:id>/", RetrieveUpdateDeleteVendorAPIView.as_view(), name="vendors_detail"),
    path("purchase_orders/", CreateListPurchaseAPIView.as_view(), name="po_get"),
    path("purchase_orders/<int:id>/", RetrieveUpdateDeletePurchaseAPIView.as_view(), name="po_detail"),
    path("vendors/<int:id>/performance", VendorPerformanceRetrieveAPIView.as_view(), name="vendor_performance"),
    path("purchase_orders/<int:id>/acknowledge", AcknowledgeAPIView.as_view(), name="po_acknowledge")
]
