from pymongo import MongoClient
from pprint import pprint
from .constrants import DB_PASSWORD

client = MongoClient(f"mongodb+srv://saedabed:{DB_PASSWORD}@cluster0.wowk8.mongodb.net/stoodfood?retryWrites=true&w=majority&authSource=admin")
db = client.stoodfood

def addRecipeToDB(recipe_name, user_id):

    db.users.update_one({
        "id": user_id
    },{
        "$set": {"last_recipe": recipe_name}
    })

def addItemToShoppingList(item, user_name):

    # db.shopping_list.insert_one({
    #     "name": item
    # })

    db.users.update_one({
        "name": user_name
    }, {
        "$push": {"cart": item}
    })

def getShoppingList(username):

    user = db.users.find_one({
        "name": username
    })
    print(user['cart'])
    return user['cart']

def addUser(name):

    userAttributes = {
        "name": name,
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
        "$push": {"inventory": item}
    })

# db.shopping_list.insert_one({
#     'name': 'tomato'
# })
#
# for item in db.shopping_list.find():
#     pprint(item)