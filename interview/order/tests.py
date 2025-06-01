from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import date
from .models import Order
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage

class DeactivateOrderViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create required inventory dependencies
        inventory_type = InventoryType.objects.create(name="Test Type")
        inventory_language = InventoryLanguage.objects.create(name="English")
        inventory = Inventory.objects.create(
            name="Test Inventory",
            type=inventory_type,
            language=inventory_language,
            metadata={"test": "data"}
        )
        
        # Create order with required fields
        self.order = Order.objects.create(
            inventory=inventory,
            start_date=date.today(),
            embargo_date=date.today(),
            is_active=True
        )
    
    def test_deactivate_order_success(self):
        url = reverse('order-deactivate', kwargs={'order_id': self.order.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
