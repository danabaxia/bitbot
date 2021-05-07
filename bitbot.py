from flaskr import app, db, db_nosql
from flaskr.models import User, Transaction, BitPrice, Balance, Product, Strategy, Order_market

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'db_nosql': db_nosql, 'User': User, 'Transaction': Transaction, 'Strategy': Strategy,
            'Balance': Balance, 'BitPrice': BitPrice, 'Product': Product, 'Market': Order_market
            }
