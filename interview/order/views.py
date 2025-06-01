from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer

class DeactivateOrderView(APIView):
    """Set the is_active state on an order"""
    def patch(self, request, order_id):
        order = generics.get_object_or_404(Order, id=order_id)
        order.is_active = False
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)
