import unittest
from inventory_manager import InventoryManager

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        self.manager = InventoryManager()
        self.manager.init_catalog([
            {"mass_g": 700, "product_name": "RBC A+ Adult", "product_id": 0},
            {"mass_g": 300, "product_name": "FFP A+", "product_id": 10}
        ])

    def test_init_catalog(self):
        self.assertEqual(len(self.manager.catalog), 2)
        self.assertEqual(self.manager.inventory[0], 0)
        self.assertEqual(self.manager.inventory[10], 0)

    def test_process_restock(self):
        restock = [{"product_id": 0, "quantity": 5}, {"product_id": 10, "quantity": 10}]
        self.manager.process_restock(restock)
        self.assertEqual(self.manager.inventory[0], 5)
        self.assertEqual(self.manager.inventory[10], 10)

    def test_process_order(self):
        self.manager.process_restock([{"product_id": 0, "quantity": 5}, {"product_id": 10, "quantity": 10}])
        order = {"order_id": 123, "requested": [{"product_id": 0, "quantity": 2}, {"product_id": 10, "quantity": 4}]}
        shipments = self.manager.process_order(order)
        self.assertEqual(len(shipments), 1)
        self.assertEqual(shipments[0]["shipped"][0]["quantity"], 2)
        self.assertEqual(shipments[0]["shipped"][1]["quantity"], 4)
        self.assertEqual(self.manager.inventory[0], 3)
        self.assertEqual(self.manager.inventory[10], 6)

if __name__ == '__main__':
    unittest.main()