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

        addItemToShoppingList()

        return []