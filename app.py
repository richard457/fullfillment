from flask import Flask, request, jsonify
from inventory_manager import InventoryManager


app = Flask(__name__)
inventory_manager = InventoryManager()

@app.route('/init_catalog', methods=['POST'])
def init_catalog():
    product_info = request.json
    inventory_manager.init_catalog(product_info)
    return jsonify({"message": "Catalog initialized successfully"}), 200

@app.route('/process_order', methods=['POST'])
def process_order():
    order = request.json
    shipments = inventory_manager.process_order(order)
    return jsonify({"message": "Order processed", "shipments": shipments}), 200

@app.route('/process_restock', methods=['POST'])
def process_restock():
    restock = request.json
    shipments = inventory_manager.process_restock(restock)
    return jsonify({"message": "Restock processed", "shipments": shipments}), 200

if __name__ == '__main__':
    app.run(debug=False)

    
