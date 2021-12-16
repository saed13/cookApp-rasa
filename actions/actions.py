# This files contains your custom actions which can be used to run
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

        print(tracker.sender_id)

        dispatcher.utter_message(msg)

        return []

class give_recipe_based_on_ingredients(Action):
    msg = ""

    def name(self) -> Text:
        return "action_return_recipe_based_on_ingredients"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        x = requests.get("")

        dispatcher.utter_message(msg)

        return []

class add_to_shopping_list(Action):

    def name(self) -> Text:
        return "action_add_selected_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        username = tracker.get_slot("name")
        print(username)
        for e in entities:
            if e['entity'] == 'item':
                item = e['value']
                addItemToShoppingList(item,username)

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
        print(username)
        if username == None:
            addUser(name)


        dispatcher.utter_message('Hello ' + name + '! How can I help you?')

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


