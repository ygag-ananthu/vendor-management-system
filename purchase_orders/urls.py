from django.urls import path
from purchase_orders.views import PurchaseOrderListView,PurchaseOrderDetailView,AcknowledgePurchaseOrderView

urlpatterns = [
    path('', PurchaseOrderListView.as_view(), name='po_list'),
    path('<int:pk>/', PurchaseOrderDetailView.as_view(), name='po_detail'),
    path('<int:pk>/acknowledge', AcknowledgePurchaseOrderView.as_view(), name='acknowledge'),
    
]