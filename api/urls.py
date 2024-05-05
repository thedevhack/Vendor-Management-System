from django.urls import path
from .views import (CreateListVendorAPIView,
                    RetrieveUpdateDeleteVendorAPIView,
                    CreateListPurchaseAPIView,
                    RetrieveUpdateDeletePurchaseAPIView,
                    VendorPerformanceRetrieveAPIView,
                    AcknowledgeAPIView)

urlpatterns = [
    path("vendors/", CreateListVendorAPIView.as_view()),
    path("vendors/<int:id>/", RetrieveUpdateDeleteVendorAPIView.as_view()),
    path("purchase_orders/", CreateListPurchaseAPIView.as_view()),
    path("purchase_orders/<int:id>/", RetrieveUpdateDeletePurchaseAPIView.as_view()),
    path("vendors/<int:id>/performance", VendorPerformanceRetrieveAPIView.as_view()),
    path("purchase_orders/<int:id>/acknowledge", AcknowledgeAPIView.as_view())
]
