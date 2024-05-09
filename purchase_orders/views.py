from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from purchase_orders.serializer import PurchaseOrderSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from purchase_orders.models import PurchaseOrder
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.permissions import IsAuthenticated

class PurchaseOrderListView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request) -> Response:
        """
        Retrieve all purchase orders.

        Returns:
            Response: The response object.
        """
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Create a new purchase order.

        Returns:
            Response: The response object.
        """
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseOrderDetailView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, pk: int) -> Response:
        """
        Retrieve a purchase order by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the purchase order.

        Returns:
            Response: The response object.
        """
        order = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseOrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk: int) -> Response:
        """
        Update a purchase order by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the purchase order.

        Returns:
            Response: The response object.
        """
        order = get_object_or_404(PurchaseOrder, pk=pk)
        serializer = PurchaseOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        """
        Delete a purchase order by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the purchase order.

        Returns:
            Response: The response object.
        """
        order = get_object_or_404(PurchaseOrder, pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AcknowledgePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def post(self, request, pk: int) -> Response:
        """
        Acknowledge a purchase order by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the purchase order.

        Returns:
            Response: The response object.
        """
        try:
            purchase_order = PurchaseOrder.objects.get(id=pk)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update acknowledgment_date
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Recalculate average_response_time for the vendor
        vendor = purchase_order.vendor
        vendor.average_response_time_calculator()
        return Response({"message": "Purchase order acknowledged successfully"})
