import json

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .database.models import setup_db, db, Drink
from .auth.auth import AuthError, requires_auth


app = Flask(__name__)
setup_db(app)
CORS(app)


@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks(payload):
    try:
        drinks = [drink.short() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception:
        return jsonify({'success': False})


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
    try:
        drinks = [drink.long() for drink in Drink.query.all()]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except Exception:
        return jsonify({
            'success': False
        })


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
    except Exception:
        db.session.rollback()
        return jsonify({
            'success': False
        })


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    try:
        request_data = request.get_json()
        drink = Drink.query.get(id)
        if not drink:
            abort(404)
        drink.title = request_data['title']
        drink.recipe = json.dumps(request_data['recipe'])
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception:
        db.session.rollback()
        return jsonify({
            'success': False
        })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    try:
        drink = Drink.query.get(drink_id)
        drink.delete()
        return jsonify({
            'success': True,
            'delete': drink.id
        })
    except Exception:
        db.session.rollback()
        return jsonify({
            'success': False
        })


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


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
