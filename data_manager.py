import requests, os


#initialize global variable
SHEETY_PRICE_ENDPOINT = os.getenv('SHEETY_FLIGHT_ENDPOINT')


class DataManager:
    def __init__(self):
        self.destination_data = {}


    def get_destination_data(self):
        '''Used to parse through Google sheet via the Sheety API. Creates a dictionary then returns the content.'''
        response = requests.get(url=SHEETY_PRICE_ENDPOINT)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data


    def update_destination_codes(self):
        '''Updates the IATA codes in the Google sheet via the Sheety API.'''
        for city in self.destination_data:
            data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(
                url=f'{SHEETY_PRICE_ENDPOINT}/{city["id"]}',
                json=data
            )
            print(response.text)


    def update_price(self):
        '''Updates the prices in the Google sheet via the Sheety API.'''
        for city in self.destination_data:
            data = {
                'price': {
                    'lowestPrice': city['lowestPrice']
                }
            }
            response = requests.put(
                url=f'{SHEETY_PRICE_ENDPOINT}/{city["id"]}',
                json=data
            )
            print(response.text)