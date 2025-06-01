from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order

class DeactivateOrderViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order = Order.objects.create(is_active=True)
    
    def test_deactivate_order_success(self):
        url = reverse('order-deactivate', kwargs={'order_id': self.order.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify order was deactivated in database
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
    
    def test_deactivate_nonexistent_order(self):
        url = reverse('order-deactivate', kwargs={'order_id': 999})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
