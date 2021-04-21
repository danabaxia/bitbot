from flaskr import app, db
from flaskr.models import User, Transaction, BitPrice, Balance, Product, Strategy

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 'Strategy': Strategy,
            'Balance': Balance, 'BitPrice': BitPrice, 'Product': Product
            }
