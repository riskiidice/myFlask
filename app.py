from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT,jwt_required
from user import UserRegister
from security import authenticate,identify

app = Flask(__name__)
app.secret_key = 'ampamp'
api = Api(app)

jwt = JWT(app, authenticate,identify)

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name']== name, items),None)
        return {'item': item }, 200 if item else 404

    def post(self, name):
        data = request.get_json()
        item = { 'name':name, 'price': data['price'] }
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        if items == None:
           return { 'items': None }, 404

        return items, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

app.run(port=5000, debug=True)
