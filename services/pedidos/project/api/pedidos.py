# services/pedidos/project/api/pedidos.py


from flask import Blueprint, jsonify, request, render_template

from project.api.models import Customer, Order, Product, Item
from project import db
from sqlalchemy import exc


pedidos_blueprint = Blueprint(
  'customers', __name__, template_folder='./templates')


@pedidos_blueprint.route('/pedidos/ping', methods=['GET'])
def ping_pong():
    return jsonify({
      'status': 'success',
      'message': 'pong'
      })


@pedidos_blueprint.route('/customers', methods=['POST'])
def add_customer():
    post_data = request.get_json()
    response_object = {
        'status': 'failed',
        'message': 'Carga invalida.'
    }
    if not post_data:
        return jsonify(response_object), 400
    names = post_data.get('names')
    try:
        customer = Customer.query.filter_by(names=names).first()
        if not customer:
            db.session.add(Customer(names=names))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{names} ha sido agregado!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Lo siento. El usuario ya existe'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@pedidos_blueprint.route('/customers/<customer_id>', methods=['GET'])
def get_single_customer(customer_id):
    """Obtener detalles de usuario único"""
    response_object = {
        'status': 'failed',
        'message': 'El customer no existe'
    }
    try:
        customer = Customer.query.filter_by(id=int(customer_id)).first()
        if not customer:
            return jsonify(response_object), 404
        else:
            response_object = {
              'status': 'success',
              'data': {
                'id': customer.id,
                'names': customer.names
              }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/customers', methods=['GET'])
def get_all_customers():
    """Obteniendo todos los customers"""
    response_object = {
        'status': 'success',
        'data': {
            'customer':
            [customer.to_json() for customer in Customer.query.all()]
        }
    }
    return jsonify(response_object), 200


@pedidos_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        names = request.form['names']
        db.session.add(Customer(names=names))
        db.session.commit()
    customer = Customer.query.all()
    return render_template('index.html', customers=customer)


@pedidos_blueprint.route('/orders/<order_id>', methods=['GET'])
def get_single_order(order_id):
    """Obtener detalles de usuario unico"""
    response_object = {
        'status': 'failed',
        'message': 'EL order no existe'
    }
    try:
        order = Order.query.filter_by(id=int(order_id)).first()
        if not order:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': order.id,
                    'customer_id': order.customer_id,
                    'date': order.date
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/orders', methods=['GET'])
def get_all_orders():
    """Obteniendo todos los orders"""
    response_object = {
        'status': 'success',
        'data': {
            'order':
            [order.to_json() for order in Order.query.all()]
        }
    }
    return jsonify(response_object), 200


@pedidos_blueprint.route('/products/<product_id>', methods=['GET'])
def get_single_item(product_id):
    """Obtener detalles de item unico"""
    response_object = {
        'status': 'failed',
        'message': 'EL product no existe'
    }
    try:
        product = Product.query.filter_by(id=int(product_id)).first()
        if not product:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': product.id,
                    'name': product.name
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/products', methods=['GET'])
def get_all_items():
    """Obteniendo todos los items"""
    response_object = {
        'status': 'success',
        'data': {
            'product':
            [product.to_json() for product in Product.query.all()]
        }
    }
    return jsonify(response_object), 200


@pedidos_blueprint.route('/items/<item_id>', methods=['GET'])
def get_singe_item(item_id):
    """Detalles item"""
    response_object = {
        'status': 'failed',
        'message': 'El item no existe'
    }
    try:
        item = Item.query.filter_by(id=int(item_id)).first()
        if not item:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': item.id,
                    'order_id': item.order_id,
                    'product_id': item.product_id,
                    'quantity': item.quantity
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pedidos_blueprint.route('/items', methods=['GET'])
def get_all_item():
    """Ontener item"""
    response_object = {
        'status': 'success',
        'data': {
            'item':
            [item.to_json() for item in Item.query.all()]
        }
    }
    return jsonify(response_object), 200
