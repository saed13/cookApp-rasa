from pymongo import MongoClient
from pprint import pprint
from .constrants import DB_PASSWORD

client = MongoClient(f"mongodb+srv://saedabed:{DB_PASSWORD}@cluster0.wowk8.mongodb.net/stoodfood?retryWrites=true&w=majority&authSource=admin")
db = client.stoodfood

def addRecipeToDB(recipe_name, user_id):

    db.users.update_one({
        "id": user_id
    },{
        "last_recipe": recipe_name
    })

def addItemToShoppingList(item, user_id):

    db.users.update_one({
        "id": user_id
    }, {
        "cart": {"$push": item}
    })

def getShoppingList(user_id):

    user = db.users.find_one({
        "id": user_id
    })

    return user.cart

def addUser(attributes):

    userAttributes = {
        "cart": [],
        "inventory": [],
        "last_recipe": None
    }

    db.users.insert_one(userAttributes)

def getUser(user_name):

    foundUser = db.users.find_one({
        "name": user_name
    })

    return foundUser

def addToInventory(item, user_id):
from pymongo import MongoClient
from pprint import pprint
from .constrants import DB_PASSWORD

client = MongoClient(f"mongodb+srv://saedabed:{DB_PASSWORD}@cluster0.wowk8.mongodb.net/stoodfood?retryWrites=true&w=majority&authSource=admin")
db = client.stoodfood

def addRecipeToDB(recipe_name, user_id):

    db.users.update_one({
        "id": user_id
    },{
        "last_recipe": recipe_name
    })

def addItemToShoppingList(item, user_id):

    db.users.update_one({
        "id": user_id
    }, {
        "cart": {"$push": item}
    })

def getShoppingList(user_id):

    user = db.users.find_one({
        "id": user_id
    })

    return user.cart

def addUser(attributes):

    userAttributes = {
        "cart": [],
        "inventory": [],
        "last_recipe": None
    }

    db.users.insert_one(userAttributes)

def getUser(user_name):

    foundUser = db.users.find_one({
        "name": user_name
    })

    return foundUser

def addToInventory(item, user_id):

    db.users.update_one({
        "id": user_id,
    }, {
        "inventory": {"$push": item}
    })

# db.shopping_list.insert_one({
#     'name': 'tomato'
# })
#
# for item in db.shopping_list.find():
#     pprint(item)