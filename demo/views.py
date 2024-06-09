import json
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .hotel import Hotel
from .room import Room
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Plan
from .serializers import PlanSerializers
from rest_framework.generics import ListAPIView,CreateAPIView,DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import requests



amadeus = Client(client_id='d0e64LqY4WYl0De6O0xfc5nq2Lp82kdu', client_secret='6rSoF5CXVQvQrsum')

zisan = {}  # Declare an empty dictionary globally

zulfiker = {} 

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def create(request):
    if request.method == 'POST':
        origin = request.POST.get('origin')
        checkin_date = request.POST.get('checkinDate')
        checkout_date = request.POST.get('checkoutDate')
        
        # Print the received data
        print("Origin:", origin)
        print("Checkin Date:", checkin_date)
        print("Checkout Date:", checkout_date)
        
        # You can perform further processing here if needed
        
        return JsonResponse({'message': 'Data received successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def fetch_data_and_store():
    global zulfiker
    url = 'http://127.0.0.1:8000/list/'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)
            for item in data:
                # Check if both 'key' and 'value' keys are present in the item
                if 'key' in item and 'value' in item:
                    zulfiker[item['key']] = item['value']
                else:
                    print("Malformed data: 'key' or 'value' missing in item:", item)
        else:
            print("Failed to fetch data. Status code:", response.status_code)
    except requests.RequestException as e:
        print("Error fetching data:", e)

# Call the function to fetch and store the data

fetch_data_and_store()

# Print the global dictionary zisan
print("Global dictionary zisan:\n", zulfiker)

class PlanCreate(CreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializers

class PlanList(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializers

class PlanListAPIView(APIView):
    def get(self, request, format=None):
        queryset = Plan.objects.all()
        serializer = PlanSerializers(queryset, many=True)
        print(serializer.data)  # Print the serialized data
        return Response(serializer.data)  


def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)  # Print the serialized data
        return Response(serializer.data)
           


class PlanDelete(DestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializers


def display_posted_data(request):
    if request.method == 'POST':
        origin = request.POST.get('Origin')
        checkinDate = request.POST.get('Checkindate')
        checkoutDate = request.POST.get('Checkoutdate')
        
        # Print the submitted data
        print("Origin:", origin)
        print("Checkin Date:", checkinDate)
        print("Checkout Date:", checkoutDate)
        
        # Add your further logic here
        # For example, you can return a JsonResponse
        return JsonResponse({'message': 'Data received successfully'}, status=200)





def demo(request):
    # global zulfiker
    # print (zulfiker.origin)
    
    # if request.method == 'POST':
    #     origin = request.POST.get('Origin')
    #     checkinDate = request.POST.get('Checkindate')
    #     checkoutDate = request.POST.get('Checkoutdate')
        
    #     # Print the submitted data
    #     print("Origin:", origin)
    #     print("Checkin Date:", checkinDate)
    #     print("Checkout Date:", checkoutDate)
        
    #     # Add your further logic here
    #     # For example, you can return a JsonResponse
    #     return JsonResponse({'message': 'Data received successfully'}, status=200)


 

# Call the function to fetch and store the data

    origin = request.POST.get('Origin')
    checkinDate = request.POST.get('Checkindate')
    checkoutDate = request.POST.get('Checkoutdate')



    kwargs = {'cityCode': origin,
              'checkInDate': checkinDate,
              'checkOutDate': checkoutDate}

    if origin and checkinDate and checkoutDate:
        try:
            # Hotel List
            hotel_list = amadeus.reference_data.locations.hotels.by_city.get(cityCode=origin)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, 'demo/demo_form.html', {})
        hotel_offers = []
        hotel_ids = []
        for i in hotel_list.data:
            hotel_ids.append(i['hotelId'])
        num_hotels = 40
        kwargs = {'hotelIds': hotel_ids[0:num_hotels],
                  'checkInDate': checkinDate,
                  'checkOutDate': checkoutDate}
        try:
            # Hotel Search
            search_hotels = amadeus.shopping.hotel_offers_search.get(**kwargs)
            print(search_hotels)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
            return render(request, 'demo/demo_form.html', {})
        try:
            global zisan  # Declare that you are using the global variable zisan
            for hotel in search_hotels.data:
                hotel_id = hotel.get('hotel', {}).get('hotelId')
                zisan[hotel_id] = hotel
                # print(zisan)
                offer = Hotel(hotel).construct_hotel()
                hotel_offers.append(offer)
                response = zip(hotel_offers, search_hotels.data)

            return render(request, 'demo/results.html', {'response': response,
                                                          'origin': origin,
                                                          'departureDate': checkinDate,
                                                          'returnDate': checkoutDate,
                                                          })
        except UnboundLocalError:
            messages.add_message(request, messages.ERROR, 'No hotels found.')
            return render(request, 'demo/demo_form.html', {})
    return render(request, 'demo/demo_form.html', {})

# demo(request)

def get_zisan(request):
    global zisan
    print(f'printing\n printing\n {zisan}')
    
    return JsonResponse(zisan)

def rooms_per_hotel(request, hotel, departureDate, returnDate):
    try:
        # Search for rooms in a given hotel
        rooms = amadeus.shopping.hotel_offers_search.get(hotelIds=hotel,
                                                           checkInDate=departureDate,
                                                           checkOutDate=returnDate).data
        hotel_rooms = Room(rooms).construct_room()
        return render(request, 'demo/rooms_per_hotel.html', {'response': hotel_rooms,
                                                             'name': rooms[0]['hotel']['name'],
                                                             })
    except (TypeError, AttributeError, ResponseError, KeyError) as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'demo/rooms_per_hotel.html', {})


def book_hotel(request, offer_id):
    try:
        # Confirm availability of a given offer
        offer_availability = amadeus.shopping.hotel_offer_search(offer_id).get()
        if offer_availability.status_code == 200:
            guests = [{'id': 1, 'name': {'title': 'MR', 'firstName': 'BOB', 'lastName': 'SMITH'},
                       'contact': {'phone': '+33679278416', 'email': 'bob.smith@email.com'}}]

            payments = {'id': 1, 'method': 'creditCard',
                        'card': {'vendorCode': 'VI', 'cardNumber': '4151289722471370', 'expiryDate': '2027-08'}}
            booking = amadeus.booking.hotel_bookings.post(offer_id, guests, payments).data
        else:
            return render(request, 'demo/booking.html', {'response': 'The room is not available'})
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, 'demo/booking.html', {})
    return render(request, 'demo/booking.html', {'id': booking[0]['id'],
                                                 'providerConfirmationId': booking[0]['providerConfirmationId']
                                                 })


def city_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None),
                                                        subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error.response.body)
    return HttpResponse(get_city_list(data), 'application/json')


def get_city_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode'] + ', ' + data[i]['name'])
    result = list(dict.fromkeys(result))
    return json.dumps(result)
