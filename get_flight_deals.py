from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager


#initilize global variableS
ORIGINAL_CITY_IATA = 'ORD'
TOMORROW = datetime.now() + timedelta(days=1)
FOUR_MONTHS_OUT = datetime.now() + timedelta(days=(4 * 30))


#create variables for imported classes
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()


#if IATA code is blank in Google sheet then proceed to update the IATA code
if sheet_data[0]['iataCode'] == '':
    for row in sheet_data:
        row['iataCode'] = flight_search.get_destination_code(row['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()


#compare Google sheets input low prices to current world prices. if current world prices are lower than Google sheets low prices then send text message with
#relevant information.
for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGINAL_CITY_IATA,
        destination['iataCode'],
        from_time=TOMORROW,
        to_time=FOUR_MONTHS_OUT
    )
    
    if flight.price < destination['lowestPrice']:
        notification_manager.send_sms(
            message=f'Low price alert! ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}.You would leave on {flight.out_date} and return 7 days later.'
        )