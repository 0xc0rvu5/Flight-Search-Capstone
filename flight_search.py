import requests, os
from flight_data import FlightData


#initialize global variables
TEQUILA_ENDPOINT_L = os.getenv('TEQUILA_ENDPOINT_LOCATION')
TEQUILA_ENDPOINT_S = os.getenv('TEQUILA_ENDPOINT_SEARCH')
TEQUILA_API_KEY = os.getenv('TEQUILA_API')
HEADERS = {'apikey': TEQUILA_API_KEY}


class FlightSearch:    
    def get_destination_code(self, city_name):
        '''Uses the Tequila API and returns the relevant IATA code for the supplied city. Paramater: city_name'''
        query = {
            'term': city_name, 
            'location_types': 'city'
            }
        response = requests.get(
            url=TEQUILA_ENDPOINT_L, 
            headers=HEADERS, 
            params=query)
        iata_code = response.json()['locations'][0]['code']
        return iata_code


    def check_flights(self, original_city_code, destination_city_code, from_time, to_time):
        '''Obtain all relevant data for future flights and output to terminal. If conditions met send text message(s). Paramaters: original_city_code, destiniation_city_code, from_time, to_time'''
        query = {
            'fly_from': original_city_code,
            'fly_to': destination_city_code,
            'date_from': from_time.strftime('%d/%m/%Y'),
            'date_to': to_time.strftime('%d/%m/%Y'),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'flight_type': 'round',
            'one_for_city': 1,
            'max_stopovers': 0,
            'curr': 'USD'
            }
        
        response = requests.get(
            url=TEQUILA_ENDPOINT_S, 
            headers=HEADERS, 
            params=query)


        try:
            data = response.json()['data'][0]
        except IndexError:
            print(f'No flights found for {destination_city_code}.')
        
        
        #parse json data variable to get all relevant data needed for program functionality.
        flight_data = FlightData(
            price=data['price'],
            origin_city=data['route'][0]['cityFrom'],
            origin_airport=data['route'][0]['flyFrom'],
            destination_city=data['route'][0]['cityTo'],
            destination_airport=data['route'][0]['flyTo'],
            out_date=data['route'][0]['local_departure'].split('T')[0],
            return_date=data['route'][0]['local_arrival'].split('T')[0]
        )

        print(f'{flight_data.destination_city}: ${flight_data.price}')
        return flight_data