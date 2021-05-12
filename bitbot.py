from flaskr import app, db, mongo
from flaskr.models import User, Transaction, Strategy, Balance, BitPrice, Product, Test, Order, Copy

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'mongo': mongo, 'User': User, 'Transaction': Transaction, 'Strategy': Strategy,
            'Balance': Balance, 'BitPrice': BitPrice, 'Product': Product, 'Test': Test, 
            'Order':Order, 'Copy':Copy
            }
 