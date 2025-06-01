from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Inventory, InventoryType, InventoryLanguage


class InventoryPaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create required foreign key objects
        self.inventory_type = InventoryType.objects.create(name="Test Type")
        self.inventory_language = InventoryLanguage.objects.create(name="English")
        
        # Create 5 inventory items to test pagination
        for i in range(5):
            Inventory.objects.create(
                name=f"Item {i+1}",
                type=self.inventory_type,
                language=self.inventory_language,
                metadata={"test": f"data{i+1}"}
            )
    
    def test_pagination_default_limit(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # Default limit is 3
    
    def test_pagination_with_offset(self):
        url = reverse('inventory-list')
        response = self.client.get(url, {'limit': 2, 'offset': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)