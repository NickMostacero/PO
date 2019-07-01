# services/pedidos/manage.py


import unittest
import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/test/*',
        'project/config.py',
    ]
)
COV.start()

from flask.cli import FlaskGroup

from project import create_app, db # nuevo
from project.api.models import Customer,Product,Order,Item

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Ejecutar las pruebas sin covertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command('seed_db')
def seed_db():
    """Sembrado en la base de datos"""
    db.session.add(Customer(names='nickmostacero'))
    db.session.add(Customer(names='ldramostacero'))
    db.session.add(Order(customer_id='1', date='01/09/09'))
    db.session.add(Order(customer_id='2', date='01/09/09'))
    db.session.add(Product(name='agua'))
    db.session.add(Product(name='gaseosa'))
    db.session.add(Item(order_id='1',product_id='1', quantity='20'))
    db.session.add(Item(order_id='2',product_id='2', quantity='21'))
    db.session.commit()


@cli.command()
def cov():
    """Ejecuta las pruebas unitarias"""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de cobertura')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)


if __name__ == '__main__':
   cli()