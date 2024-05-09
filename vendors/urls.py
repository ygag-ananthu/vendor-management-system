from django.urls import path
from vendors.views import VendorListView,VendorDetailView,VendorPerformanceView

urlpatterns = [
    path('', VendorListView.as_view(), name='vendor_list'),
    path('<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('<int:pk>/performance', VendorPerformanceView.as_view(), name='vendor_performance'),
]