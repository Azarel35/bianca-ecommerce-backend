from flask  import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os  

app = Flask(__name__)


basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
   
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password 
       

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id','name', 'email', 'password')
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    

    def __init__(self, name, description, price, category):
        self.name = name
        self.description = description
        self.price = price 
        self.category = category


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'category')
    
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)

    def __init__(self, street, number, city):
        self.street = street
        self.number = number
        self.city = city 

class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id','street', 'number', 'city')
    
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String, nullable=False)
    total = db.Column(db.String, nullable=False)
    

    def __init__(self, quantity, total):
        self.quantity = quantity
        self.total = total
        

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id','quantity', 'total')
    
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/user', methods=["POST"])
def add_user():
    name = request.json.get("name")
    email = request.json.get("email")
    password = request.json.get("password")

    new_user = User(name, email, password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))

@app.route("/users", methods=["GET"])
def get_all_users():
    all_users  = User.query.all()
    return jsonify(users_schema.dump(all_users))

@app.route('/login', methods=["POST"])
def read_user():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user.password == password:
             return  jsonify({"user_email": user.email}) 
        else:
              return jsonify({'Message': "wrong password", 'successful': False})
    else :
        return jsonify({'Message': "User not found.", 'successful': False})

@app.route('/product', methods=["POST"])
def add_product():
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    category = request.json.get("category")

    new_product = Product(name, description, price, category)
    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product))

@app.route("/products", methods=["GET"])
def get_all_products():
    all_products  = Product.query.all()
    return jsonify(products_schema.dump(all_products))

@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/address', methods=["POST"])
def add_address():
    street = request.json.get("street")
    number = request.json.get("number")
    city = request.json.get("city")
   
    new_address = Address(street, number, city)
    db.session.add(new_address)
    db.session.commit()

    return jsonify(address_schema.dump(new_address))

@app.route("/addresses", methods=["GET"])
def get_all_addresses():
    all_addresses  = Address.query.all()
    return jsonify(addresses_schema.dump(all_addresses))

@app.route('/order', methods=["POST"])
def add_order():
    quantity = request.json.get("quantity")
    total = request.json.get("total")

    new_order = Order(quantity, total)
    db.session.add(new_order)
    db.session.commit()

    return jsonify(order_schema.dump(new_order))

@app.route("/orders", methods=["GET"])
def get_all_orders():
    all_orders  = Order.query.all()
    return jsonify(orders_schema.dump(all_orders))

if __name__=='__main__':
    app.run(debug=True)