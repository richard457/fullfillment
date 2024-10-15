from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventoryManager:
    MAX_PACKAGE_WEIGHT = 1800  # 1.8kg in grams

    def __init__(self):
        self.catalog = {}
        self.inventory = {}
        self.pending_orders = []

    def init_catalog(self, product_info: List[Dict]):
        for product in product_info:
            self.catalog[product['product_id']] = product
            self.inventory[product['product_id']] = 0
        logger.info("Catalog initialized with %d products", len(product_info))

    def process_order(self, order: Dict) -> List[Dict]:
        order_id = order['order_id']
        requested = order['requested']
        
        shipments = self._create_shipments(order_id, requested)
        
        if not all(item['quantity'] == 0 for item in requested):
            self.pending_orders.append({'order_id': order_id, 'requested': requested})
            logger.info("Order %d partially fulfilled and added to pending orders", order_id)
        else:
            logger.info("Order %d fully fulfilled", order_id)
        
        return shipments

    def process_restock(self, restock: List[Dict]) -> List[Dict]:
        for item in restock:
            product_id = item['product_id']
            quantity = item['quantity']
            self.inventory[product_id] += quantity
        
        logger.info("Restock processed: %s", restock)
        
        return self._process_pending_orders()

    def _create_shipments(self, order_id: int, requested: List[Dict]) -> List[Dict]:
        shipments = []
        current_shipment = {"order_id": order_id, "shipped": []}
        current_weight = 0

        for item in requested:
            product_id = item['product_id']
            quantity = item['quantity']
            product_weight = self.catalog[product_id]['mass_g']

            while quantity > 0 and self.inventory[product_id] > 0:
                if current_weight + product_weight > self.MAX_PACKAGE_WEIGHT:
                    shipments.append(current_shipment)
                    current_shipment = {"order_id": order_id, "shipped": []}
                    current_weight = 0

                ship_quantity = min(quantity, self.inventory[product_id])
                current_shipment["shipped"].append({"product_id": product_id, "quantity": ship_quantity})
                current_weight += product_weight * ship_quantity
                self.inventory[product_id] -= ship_quantity
                quantity -= ship_quantity

            # Update item['quantity'] after the loop finishes
            item['quantity'] = quantity

        if current_shipment["shipped"]:
            shipments.append(current_shipment)

        for shipment in shipments:
            self._ship_package(shipment)

        return shipments

    def _process_pending_orders(self) -> List[Dict]:
        shipments = []
        fulfilled_orders = []

        for order in self.pending_orders:
            order_shipments = self._create_shipments(order['order_id'], order['requested'])
            shipments.extend(order_shipments)
            
            if all(item['quantity'] == 0 for item in order['requested']):
                fulfilled_orders.append(order)

        for order in fulfilled_orders:
            self.pending_orders.remove(order)

        return shipments

    def _ship_package(self, shipment: Dict):
        logger.info("Shipping package: %s", shipment)
        # In a real application, this would interface with a shipping system
        # For now, we're just logging the shipment