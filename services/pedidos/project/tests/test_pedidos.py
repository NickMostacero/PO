# services/pedidos/project/tests/test_pedidos.py


import json
import unittest
from project import db
from project.api.models import Customer, Order
from project.tests.base import BaseTestCase


def add_customer(name):
    customer = Customer(names=name)
    db.session.add(customer)
    db.session.commit()
    return customer


def add_order(id_customer, date):
    order = Order(id_customer=id_customer, date=date)
    db.session.add(order)
    db.session.commit()
    return order


class TestPedidosService(BaseTestCase):
    """Tests for the Users Service."""

    def test_pedidos(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/pedidos/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_customer(self):
        """Agregando un nuevo cliente."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'names': 'nickmostacero'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('nickmostacero ha sido agregado!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_customer_invalid_json(self):
        """Asegurando que se produzca un error si el objeto json esta vacío."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Carga invalida.', data['message'])
            self.assertIn('failed', data['status'])

    def test_add_customer_duplicate_name(self):
        """Asegurando que se produzca un error si el nombre ya existe."""
        with self.client:
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'names': 'nickmostacero'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/customers',
                data=json.dumps({
                    'names': 'nickmostacero'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Lo siento. El usuario ya existe', data['message'])
            self.assertIn('failed', data['status'])

    def test_single_customer(self):
        """Asegurando que obtenga un customer de forma correcta"""
        customer = add_customer(name="nickmostacero")
        with self.client:
            response = self.client.get(f'/customers/{customer.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('nickmostacero', data['data']['names'])
            self.assertIn('success', data['status'])

    def test_single_customer_no_id(self):
        """Asegúrese de que se arroje un error si no
        se proporciona una identificación"""
        with self.client:
            response = self.client.get('/customers/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El customer no existe', data['message'])
            self.assertIn('failed', data['status'])

    def test_single_customer_incorrect_id(self):
        """Asegurando de que se arroje un error si
        la identificación no existe"""
        with self.client:
            response = self.client.get('/customers/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('El customer no existe', data['message'])
            self.assertIn('failed', data['status'])

    def test_all_customer(self):
        """ Asegurando de que todos los usuarios se comporten correctamente."""
        add_customer('nickmostacero')
        add_customer('bramostacero')
        with self.client:
            response = self.client.get('/customers')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['customer']), 2)
            self.assertIn(
                'nickmostacero', data['data']['customer'][0]['names'])
            self.assertIn('bramostacero', data['data']['customer'][1]['names'])
            self.assertIn('success', data['status'])

    def test_main_no_users(self):
        """ La ruta principal funciona? con clientes añadidos a la db."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Todos los clientes', response.data)
        self.assertIn(b'<p>No hay clientes!</p>', response.data)

    def test_main_with_users(self):
        """ La ruta principal funciona? cuando un usuario es add ."""
        add_customer('nickmostacero')
        add_customer('bramostacero')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los clientes', response.data)
            self.assertNotIn(b'<p>No hay clientes!</p>', response.data)
            self.assertIn(b'nickmostacero', response.data)
            self.assertIn(b'bramostacero', response.data)

    def test_main_add_users(self):
        """ Un nuevo cliente puede add a la db mediante un POST request? ."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(names='nickmostacero'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Todos los clientes', response.data)
            self.assertNotIn(b'<p>No hay clientes!</p>', response.data)
            self.assertIn(b'nickmostacero', response.data)


if __name__ == '__main__':
    unittest.main()
