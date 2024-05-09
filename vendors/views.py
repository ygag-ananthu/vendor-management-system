from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from vendors.models import Vendor
from vendors.serializer import VendorSerializer
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class VendorDetailView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def delete(self, request, pk: int) -> Response:
        """
        Delete a vendor by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the vendor.

        Returns:
            Response: The response object.
        """
        vendor = get_object_or_404(Vendor, pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, pk: int) -> Response:
        """
        Retrieve a vendor by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the vendor.

        Returns:
            Response: The response object.
        """
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, pk: int) -> Response:
        """
        Update a vendor by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the vendor.

        Returns:
            Response: The response object.
        """
        vendor = get_object_or_404(Vendor, pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorListView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request) -> Response:
        """
        Retrieve all vendors.

        Args:
            request: The request object.

        Returns:
            Response: The response object.
        """
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request) -> Response:
        """
        Create a new vendor.

        Args:
            request: The request object.

        Returns:
            Response: The response object.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorPerformanceView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, pk: int) -> Response:
        """
        Retrieve performance metrics for a vendor by its primary key.

        Args:
            request: The request object.
            pk (int): The primary key of the vendor.

        Returns:
            Response: The response object.
        """
        try:
            vendor = Vendor.objects.get(id=pk)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        performance_metrics = {
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate
        }

        return Response(performance_metrics)
