import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from werkzeug.exceptions import NotFound

from .database.models import setup_db, db, Drink, db_drop_and_create_all
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception as e:
        print(e)
        abort(500)


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except AuthError as e:
        raise e
    except Exception:
        abort(500)


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drink(payload):
    try:
        request_data = request.get_json()
        drink = Drink()
        drink.title = request_data['title']
        drink.recipe = json.dumps(request_data['recipe'])
        drink.insert()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except AuthError as e:
        raise e
    except Exception:
        db.session.rollback()
        abort(422)


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        request_data = request.get_json()
        drink = Drink.query.get(id)
        if not drink:
            abort(404)
        drink.title = request_data.get('title', drink.title)
        drink.recipe = json.dumps(request_data.get('recipe', drink.recipe))
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except AuthError as e:
        raise e
    except NotFound:
        abort(404)
    except Exception:
        db.session.rollback()
        abort(422)


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.get(drink_id)
        if not drink:
            abort(404)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id
        })
    except AuthError as e:
        raise e
    except NotFound:
        abort(404)
    except Exception:
        db.session.rollback()
        abort(500)


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def notfound(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@app.errorhandler(AuthError)
def autherror(error):
    return jsonify({
        'success': False,
        'error': 'auth error',
        'message': 'Authentication error'
    }), 401


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'internal server error'
    }), 500
