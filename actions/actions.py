from typing import Any, Text, Dict, List
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
import logging
from rasa_sdk.types import DomainDict

logger = logging.getLogger(__name__)

class PerformCurrencyConversion(Action):

    def name(self) -> Text:
        return "action_perform_currency_conversion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:


        from_currency = tracker.get_slot('from_currency')
        to_currency = tracker.get_slot('to_currency')
        amount_to_convert = tracker.get_slot('amount_to_convert')

        response_message = f"Extracted entities - Amount to convert: {amount_to_convert}, original currency : {from_currency}, to_currency : {to_currency}"


        amount_to_convert = float(amount_to_convert)
        API_KEY = '9ce3b3bd9b0f69be1a3bec0d'
        BASE_URL = f'https://v6.exchangerate-api.com/v6/9ce3b3bd9b0f69be1a3bec0d/latest/'

        response = requests.get(BASE_URL + from_currency)
        if response.status_code == 200:
            exchange_data = response.json()
        else:
            exchange_data = None

        if exchange_data:
            rates = exchange_data['conversion_rates']
            if to_currency in rates:
                converted_amount = amount_to_convert * rates[to_currency]
            else:
                print(f"Error: {to_currency} not found in exchange rates.")
                return []
        else:
            print("Error : unable to extract exchange rates.")
            return []
        dispatcher.utter_message(
            text=f"{amount_to_convert} {from_currency} is equal to {converted_amount} {to_currency}.")

        return []

class ActionResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("amount_to_convert", None), SlotSet("from_currency", None), SlotSet("to_currency", None)]

class ExtractLocation(Action):
    def name(self) -> Text:
        return "action_extract_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']
        #
        # street_name= ""
        # street_n= ""
        # street_number = ""
        # city = ""
        #
        # for entity in entities:
        #     if entity['entity'] == 'street_name':
        #         street_name = entity['value']
        #     elif entity['entity'] == 'street_n':
        #         street_n = entity['value']
        #     elif entity['entity'] == 'street_number':
        #         street_number = entity['value']
        #     elif entity['entity'] == 'city':
        #         city = entity['value']
        #
        # # location = f"{street_number}, {street_n}, {street_name}, {city}"
        # # # location = str(street_number) +street_n + street_name + city
        # # dispatcher.utter_message(text=f"D'accord ! Je cherche des distributeurs automatiques près de {location}. ")
        # dispatcher.utter_message(text=f"{city}")








        # try:
        #
        #     location = tracker.latest_message['entities'][0]['value']
        #
        # except:
        #     location = None
        #
        # if location:
        # dispatcher.utter_message(text=f"D'accord ! Je cherche des distributeurs automatiques près de {location}. ")
        # else:
        # dispatcher.utter_message(text="Sorry, I couldn't find a location in your message. Please try again.")
            # return []

        return []


class FindATMWithCurrentLocation(Action):
    def name(self) -> Text:
        return "action_find_atm_with_current_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        latitude, longitude = data['loc'].split(',')
        api_key = "EiQLX9cU9W85SCd9jA6DCvEAE-YMoyUBqTdgthwrsnI"
        dispatcher.utter_message(text=f"IP: {data['ip']}, City: {data['city']}, Region: {data['region']}, Country: {data['country']}, Location: {data['loc']}")
        radius = "1000"
        categories = "600-6600-0575"  # Category ID for ATM

        url = f"https://discover.search.hereapi.com/v1/discover?at={latitude},{longitude}&limit=10&q=atm&lang=en-US&apiKey={api_key}"

        response = requests.get(url)
        data = response.json()

        if 'items' in data:
            for item in data['items']:
                dispatcher.utter_message(text= f"ATM : {item['title']} / Location : {item['address']['label']}")
        else:
            dispatcher.utter_message(text= "No ATMs found.")



class TransferMoney(Action):
    def name(self) -> Text:
        return "action_transfer_money"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        # entities = tracker.latest_message['entities']
        #
        # recipient = None
        # amount_to_send = None
        #
        # for entity in entities:
        #     if entity['entity'] == 'amount_to_send':
        #         amount_to_send = entity['value']
        #     elif entity['entity'] == 'recipient':
        #         recipient = entity['value']
        recipient = tracker.get_slot('recipient')
        amount_to_send = tracker.get_slot('amount_to_send')

        response_message = f"Extracted entities - Amount to send: {amount_to_send}, recipient : {recipient}\n voulez vous effectuer un virement ponctuel ou permanent"
        dispatcher.utter_message(text=response_message)
        return []

class PhoneNumber(Action):
    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        last_name = tracker.get_slot('last_name')
        name = tracker.get_slot('name')


        dispatcher.utter_message(text=f"your name is {name} and your last name is {last_name}")

        return[]


class AccountNumber(Action):
    def name(self) -> Text:
        return "action_retrieve_accounts"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Here is the list of your accounts. Which one would you like to choose?")

        nom = tracker.latest_message['entities'][0]['value']

        SlotSet("nom", nom)

        url = f"http://127.0.0.1:8080/accounts/{nom}"

        response = requests.get(url)
        global accounts
        accounts = response.json()['accounts']
        if not accounts:
            dispatcher.utter_message(text="No accounts found")
            return []
        if response.status_code == 200:
            i = 1
            for e in response.json()['accounts']:
                dispatcher.utter_message(text =f"{i}. {e}" )
                i+=1
        else:
            dispatcher.utter_message(text=f'Error:{response.status_code}' )
        return [SlotSet("nom", nom)]

class AccountBalance(Action):
    def name(self) -> Text:
        return "action_balance"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        nb = None
        # Iterate over entities to find the 'nb' entity
        for entity in tracker.latest_message.get('entities', []):
            if entity.get('entity') == 'nb':
                nb = entity.get('value')

        # If the entity is not found or is invalid
        if nb is None:
            dispatcher.utter_message(text="Sorry, I didn't understand your selection.")
            return []


        nb = int(nb)
        # dispatcher.utter_message(text=f"{nb} is your nb")

        global accounts
        if nb < 1 or nb > len(accounts):
            dispatcher.utter_message(text="Invalid selection.")
            return []

        account_id = accounts[nb - 1]
        nom = tracker.get_slot('nom')
        url = f"http://127.0.0.1:8080/accounts/{nom}/{account_id}"
        response = requests.get(url)
        balance = response.json()['balance']
        dispatcher.utter_message(text=f"The balance of the account \"{account_id}\" is : {balance}.")


class ActionCustomFallback(Action):
    def name(self) -> Text:
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

       dispatcher.utter_message(text="Sorry, I didn't understand")

       unrecognized_message = tracker.latest_message.get('text')

       conn = sqlite3.connect('unrecognized_intents.db')
       cursor = conn.cursor()

       cursor.execute('''CREATE TABLE IF NOT EXISTS unrecognized_intents
                                 (message TEXT)''')

       cursor.execute("INSERT INTO unrecognized_intents (message) VALUES (?)", (unrecognized_message,))
       conn.commit()
       conn.close()

