# This files contains your custom actions which can be used to run
import random

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, events
from rasa_sdk.executor import CollectingDispatcher
from .connectDB import *
from .constrants import API_KEY
from rasa.shared.core.slots import Slot

def listToString(s):
    # initialize an empty string
    str1 = ", "

    # return string
    return (str1.join(s))
def listToAPI(s):
    # initialize an empty string
    str1 = ",+"

    # return string
    return (str1.join(s))
#get sender id, save it in the DB
class give_recommendation(Action):
    msg = ""

    def name(self) -> Text:
        return "action_return_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        ploads = {'apiKey' : API_KEY, 'number':1}
        x = requests.get('https://api.spoonacular.com/recipes/random', params=ploads)
        resDic = x.json()
        msg = resDic['recipes'][0]['title']

        #addRecipeToDB(msg)


        dispatcher.utter_message("here's your recipe "+msg+" "+resDic['recipes'][0]['spoonacularSourceUrl'])

        return []

class give_recommendation_based_on_diet(Action):
    msg = ""

    def name(self) -> Text:
        return "action_return_recipe_based_on_diet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], diet=None) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        username = tracker.get_slot("name")
        for e in entities:
            if e['entity'] == 'diet':
                diet = e['value']
        if(diet!=None):
            ploads = {'apiKey' : API_KEY, 'diet': diet}
            x = requests.get('https://api.spoonacular.com/recipes/complexSearch', params=ploads)
            resDic = x.json()
            recipePos = random.randint(0, len(resDic['results']) - 1)
            recipeID = resDic['results'][recipePos]['id']
            recipeID=str(recipeID)
            y = requests.get('https://api.spoonacular.com/recipes/'+recipeID+'/information', params={
                'apiKey': API_KEY
            })
            resDicY= y.json()
            msg = resDic['results'][recipePos]['title']

            #addRecipeToDB(msg)

            dispatcher.utter_message("That's the recipe: "+msg+" and here's the link so you can enjoy it: "+resDicY['spoonacularSourceUrl'])
        else:
            ploads = {'apiKey': API_KEY, 'number': 1}
            x = requests.get('https://api.spoonacular.com/recipes/random', params=ploads)
            resDic = x.json()
            msg = resDic['recipes'][0]['title']

            # addRecipeToDB(msg)


            dispatcher.utter_message(msg)

        return []

class give_recipe_based_on_ingredients(Action):
    msg = ""

    def name(self) -> Text:
        return "action_return_recipe_based_on_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entitiesList = []
        entities = tracker.latest_message['entities']
        username = tracker.get_slot("name")
        for e in entities:
            if e['entity'] == 'item':
                item = e['value']
                entitiesList.append(item)
        if(len(entitiesList)>0):
            strList = listToAPI(entitiesList)
        else:
            strList = entitiesList

        ploads = {'apiKey': API_KEY, 'number': 2, 'ingredients': strList}
        x = requests.get('https://api.spoonacular.com/recipes/findByIngredients', params=ploads)
        resDic = x.json()
        if(len(resDic)>0):
            msg = resDic[0]['title']
            recipeID = resDic[0]['id']
            recipeID = str(recipeID)
            y = requests.get('https://api.spoonacular.com/recipes/' + recipeID + '/information', params={
                'apiKey': API_KEY
            })
            resDicY = y.json()
            dispatcher.utter_message("here's your recipe "+msg+" "+resDicY['spoonacularSourceUrl'])
        else:
            dispatcher.utter_message("No recipe found with these ingredients")

        return []

class add_to_shopping_list(Action):

    def name(self) -> Text:
        return "action_add_selected_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        username = tracker.get_slot("name")
        for e in entities:
            if e['entity'] == 'item':
                item = e['value']
                addItemToShoppingList(item, username)

        dispatcher.utter_message('okay, '+username+', I have added the items to your list')

        return []

class action_react_name(Action):

    def name(self) -> Text:
        return "action_react_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        name = ""
        for e in entities:
            if e['entity'] == 'name':
                name = e['value']

        username = getUser(name)
        if username == None:
            addUser(name)


        dispatcher.utter_message('Hello ' + name + '! How may I assist you?')

        return [events.SlotSet("name", name)]


class action_return_shopping_list(Action):

    def name(self) -> Text:
            return "action_return_shopping_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("name")

        list = getShoppingList(username)
        strList= listToString(list)


        dispatcher.utter_message('Okay, your list contains the following items:'+ strList)

        return []


