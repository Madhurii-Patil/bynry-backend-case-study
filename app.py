from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>✅ StockFlow API is Running Successfully!</h1>"

# --- FIX 1: Add Database Configuration (SQLite) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- FIX 2: Define the "Models" (So Python knows what a Product is) ---
# These act as the Python version of your SQL tables

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    sku = db.Column(db.String(100))
    price = db.Column(db.Float)
    low_stock_threshold = db.Column(db.Integer, default=10)
    company_id = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer)

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    quantity = db.Column(db.Integer)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    contact_email = db.Column(db.String(100))

# --- YOUR ORIGINAL SOLUTION CODE ---

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    
    # 1. Validation
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}, 400
    
    try:
        # 2. Create Product 
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=data['price'],
            company_id=1  # Dummy ID for testing
        )
        
        db.session.add(product)
        db.session.flush() 
        
        # 3. Create Inventory
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )
        
        db.session.add(inventory)
        db.session.commit()
        
        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    alerts = []
    try:
        low_stock_items = db.session.query(Inventory, Product, Warehouse, Supplier)\
            .join(Product, Inventory.product_id == Product.id)\
            .join(Warehouse, Inventory.warehouse_id == Warehouse.id)\
            .join(Supplier, Product.supplier_id == Supplier.id)\
            .filter(Product.company_id == company_id)\
            .filter(Inventory.quantity <= Product.low_stock_threshold)\
            .all()

        for inv, prod, wh, sup in low_stock_items:
            # Simple dummy sales velocity
            avg_daily_sales = 2.5 
            
            days_left = 0
            if inv.quantity > 0:
                days_left = inv.quantity / avg_daily_sales

            alerts.append({
                "product_name": prod.name,
                "days_until_stockout": round(days_left, 1),
                "supplier": sup.name
            })

        return {"alerts": alerts}, 200

    except Exception as e:
        return {"error": str(e)}, 500

# --- RUN BLOCK ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all() # This actually creates the 'local_inventory.db' file!
    app.run(debug=True)