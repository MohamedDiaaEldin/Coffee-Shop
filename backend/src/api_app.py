import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import  requires_auth

app = Flask(__name__)
db = setup_db(app)
CORS(app)


@app.route('/')
def index():
    return 'hi'

# db_drop_and_create_all()
# ROUTES
    
@app.route('/drinks')
def get_short_drinks():
    try:
        drinks = Drink.query.all()
        short_drinks = [drink.short() for drink in drinks]
        return  jsonify({
        'success':True,
        'drinks' : short_drinks
        })
    except :
        print('error happend')
        return abort(500)



@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_lonng_drinks(jwt):

    try:
        drinks = Drink.query.all()
        long_drinks = [drink.long() for drink in drinks]
        return  jsonify({
            'success':True,
            'drinks' : long_drinks
        })
    except :
        print('error while getting ruslts from short drinks from database')
        return abort(500)



# cola = Drink(title='cola', recipe='{"color":"black", "name":"cola", "parts":"60"}')
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(jwt):
    try:            
        body = request.get_json()
        print(json.dumps(body['recipe']))
        print(type(json.dumps(body['recipe'])))
        new_drink = Drink(title = body['title'], recipe = json.dumps(body['recipe']))
        new_drink.insert()
        return jsonify({
            'success' : True,
            'drinks' : [new_drink.long()]
        })
    except:
        db.session.rollback()
        print('error while adding new drink')
        abort(500)

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):

    try:
        body = request.get_json()        
        title = body.get('title', None)
        recipe = body.get('recipe', None)
        print(title)
        if title == None or recipe == None :
            abort(500)
        drink = Drink.query.get(int(id))
        if  drink == None :
            abort(404)
        drink.title = title
        drink.recipe = json.dumps(recipe)
        drink.update()
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        db.session.rollback()
        print('error while updating')
        abort(500)    
    

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.get(int(id))
        if  drink == None :
            abort(404)

        drink.delete()
        return jsonify({
        'success': True,
        'delete': id
    })
    except:
        print('error while updating')
        abort(500)    

# Error Handling

@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        'error' : 403 ,
        'message' :'Forbidden'
    }), 403

@app.errorhandler(400)
def permissions_not_found(error):
    return jsonify({
        'error' : 400 ,
        'message' :'Permissions not included'
    }), 400

@app.errorhandler(500)
def data_not_found(error):
    return jsonify({
        'error' : 500 ,
        'message' :'error while getting results'
    }), 500

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        'error' : 401 ,
        'message' :'Unauthorized'
    }), 401

@app.errorhandler(404)
def unauthorized(error):
    return jsonify({
        'error' : 404 ,
        'message' :'not found'
    }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422