from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, F, ExpressionWrapper, fields
from .models import Vendor, PurchaseOrder
from .serializers import (VendorSerializer,
                          PurchaseOrderSerializer,
                          VendorPerformanceSerializer)


class CreateListVendorAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class RetrieveUpdateDeleteVendorAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    lookup_field = 'id'


class CreateListPurchaseAPIView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vendor']


class RetrieveUpdateDeletePurchaseAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     if 'status' in request.data:
    #         instance.status = request.data['status']
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class VendorPerformanceRetrieveAPIView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer
    lookup_field = 'id'


class AcknowledgeAPIView(APIView):
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        pid = kwargs.get('id')
        try:
            instance = PurchaseOrder.objects.get(id=pid)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'order for the purchase id does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if instance.acknowledgment_date:
            return Response({'error': 'Already Acknowledged'}, status=status.HTTP_400_BAD_REQUEST)

        instance.acknowledgment_date = timezone.now()
        instance.save()

        """
            response time depends on seconds taken from issue date 
            till the vendor acknowledges the purchase and start the
            process to deliver it and we have taken averages
            of all such response times to get average response
            time of a vendor
        """
        average_response_time = PurchaseOrder.objects.filter(
            vendor=instance.vendor,
            acknowledgment_date__isnull=False
        ).annotate(
            response_times=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=fields.DurationField()
            )
        ).aggregate(
            total_time=Avg('response_times')
        )

        average_response_time_value = average_response_time.get('total_time', timedelta())
        average_response_time_seconds = average_response_time_value.total_seconds()
        average_response_time_float = average_response_time_seconds\
            if average_response_time_seconds is not None else 0.0

        instance.vendor.average_response_time = average_response_time_float
        instance.vendor.save()

        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
