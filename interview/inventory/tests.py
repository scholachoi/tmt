from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from .models import Inventory, InventoryType, InventoryLanguage
import time

class InventoryAfterDateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create required foreign key objects
        self.inventory_type = InventoryType.objects.create(name="Test Type")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        
        # Create old inventory
        self.old_inventory = Inventory.objects.create(
            name="Old Item",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={"test": "data"}
        )
        
        time.sleep(0.1)
        
        # Create recent inventory  
        self.recent_inventory = Inventory.objects.create(
            name="Recent Item",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={"test": "data"}
        )
    
    def test_filter_inventory_after_date(self):
        filter_date = self.old_inventory.created_at.isoformat()
        url = reverse('inventory-list')
        response = self.client.get(url, {'date': filter_date})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
