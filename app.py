from flaskfrom  import Flask, request, jsonify
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
        fields = ('id','name', 'email')
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    orders = db.relationship('Order', backref='product', lazy=True)


    def __init__(self, name, description, price):
        self.name = name
        self.description = description
        self.price = price 

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price')
    
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String, nullable=False)
    number = db.Column(db.String, nullable=False)
    postalCode = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __init__(self, street, number, postalCode, state, city, user_id):
        self.street = street
        self.number = number
        self.postalCode = postalCode
        self.state = state
        self.city = city 
        self.user_id = user_id

class AddressSchema(ma.Schema):
    class Meta:
        fields = ('id','street', 'number', 'postalCode', 'state', 'city')
    
address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.String, nullable=False)
    total = db.Column(db.String, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
        nullable=False)
    

    def __init__(self, quantity, total, date, product_id):
        self.quantity = quantity
        self.total = total
        self.date = date
        self.product_id = product_id 

class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id','quantity', 'total', 'date')
    
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
    query = "SELECT * FROM user WHERE email = '{0}' AND password ='{1}' ".format(email,password)
    results = db.session.execute(query)
    if results :
        return  jsonify({"user_data":users_schema.dump(results)}) 

    else :
        return jsonify({'Message': "User not found.", 'successful': False})

@app.route('/product', methods=["POST"])
def add_product():
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")

    new_product = Product(name, description, price)
    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product))

@app.route("/products", methods=["GET"])
def get_all_products():
    all_products  = Product.query.all()
    return jsonify(products_schema.dump(all_products))

@app.route('/address', methods=["POST"])
def add_address():
    street = request.json.get("street")
    number = request.json.get("number")
    postalCode = request.json.get("postalCode")
    state = request.json.get("state")
    city = request.json.get("city")
    user_id = request.json.get("user_id")

    new_address = Address(street, number, postalCode, state, city,user_id)
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
    date = request.json.get("date")

    new_order = Order(quantity, total, date)
    db.session.add(new_order)
    db.session.commit()

    return jsonify(order_schema.dump(new_order))

@app.route("/orders", methods=["GET"])
def get_all_orders():
    all_orders  = Order.query.all()
    return jsonify(orders_schema.dump(all_orders))



if __name__=='__main__':
    app.run(debug=True)