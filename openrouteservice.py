# connect to openrouteservice cloud, send current and goal coordinates =>recieve map route direction
import requests
import json
import struct
import bluetooth

# connect to esp32 via bluetooth
target_address = 'B8:D6:1A:43:5D:F2'
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((target_address, port))
message = 'Hello, ESP32!'
sock.send(message.encode())

# Specify the start and end locations
start_location = [8.681495, 49.41461]  # Example start location (latitude, longitude)
end_location = [8.687872, 49.420318]  # Example end location (latitude, longitude)

api_key='5b3ce3597851110001cf6248c5612d1738364a91a1c660636015a7c6'

# # Set up the API endpoint URL
# url = "https://api.openrouteservice.org/v2/directions/driving-car/realtime"

# # Set up the request headers and parameters
# headers = {'Authorization': '5b3ce3597851110001cf6248c5612d1738364a91a1c660636015a7c6', 'Content-Type': 'application/json'}
# params = {'coordinates': [start_location, end_location], 'format': 'geojson', 'instructions_format': 'text'}

# # Send the initial request to set up the navigation session
# response = requests.post(url, headers=headers, params=params)
url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={start_location[0]},{start_location[1]}&end={end_location[0]},{end_location[1]}'#my modified request code(square brackets cause an issue)
# print(url)
response=requests.get(url)
# Extract the session ID from the response
# session_id = response.json()['session_id']

# Simulate real-time GPS data by sending periodic requests with the current location
for i in range(10):
    # Example current location (latitude, longitude)
    current_location = [start_location[0] + (end_location[0] - start_location[0]) * i / 10,
                        start_location[1] + (end_location[1] - start_location[1]) * i / 10]

    # # Set up the request parameters for the current location
    # params = {'session_id': session_id, 'format': 'geojson', 'location': current_location}

    # # Send the request to get updated directions based on the current location
    # response = requests.post(url, headers=headers, params=params)



    url = f'https://api.openrouteservice.org/v2/directions/driving-car?api_key={api_key}&start={current_location[0]},{current_location[1]}&end={end_location[0]},{end_location[1]}'#my modified request code(square brackets cause an issue)
    
    response=requests.get(url)

    # Extract the next instruction from the response
    next_instruction = response.json()['features'][0]['properties']['segments'][0]['steps'][0]['instruction']

    distance_remaining=response.json()['features'][0]['properties']['segments'][0]['steps'][0]['type']
    next_instruction_index=response.json()['features'][0]['properties']['segments'][0]['steps'][0]['distance']
    
    distance_remaining_bytes=struct.pack('f', distance_remaining)
    next_instruction_index_bytes=struct.pack('f', next_instruction_index)
    # sock.send(next_instruction.encode())
    flag1=struct.pack('f', 1.0)
    flag2=struct.pack('f', 2.0)
    sock.send(flag1)
    sock.send(distance_remaining_bytes)
    sock.send(flag2)
    sock.send(next_instruction_index_bytes)
    # Print the next instruction

    print(f"Next instruction: {next_instruction}")
