from flaskr import app, db
from flaskr.models import User, Transaction, Product, Strategy, BitPrice

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 
                      'Product': Product, 'Strategy': Strategy, 'BitPrice': BitPrice}
