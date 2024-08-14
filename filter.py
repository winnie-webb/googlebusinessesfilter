import requests

def get_places(api_key, location, radius, query):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': query,
        'location': location,
        'radius': radius,
        'key': api_key
    }

    print(f"Fetching places with URL: {url} and parameters: {params}")
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Successfully fetched places.")
        data = response.json()
        if data.get('status') == 'REQUEST_DENIED':
            print(f"Request denied: {data.get('error_message')}")
            return None
        return data
    else:
        print(f"Error fetching places: {response.status_code} - {response.text}")
        return None

def get_place_details(api_key, place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': place_id,
        'key': api_key
    }

    print(f"Fetching details for place ID: {place_id} with URL: {url} and parameters: {params}")
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Successfully fetched place details.")
        return response.json().get('result')
    else:
        print(f"Error fetching place details: {response.status_code} - {response.text}")
        return None

def main():
    # Replace with your actual API key
    api_key = 'API_KEY'
    location = '37.7749,-122.4194'  # Latitude and Longitude for San Francisco, CA
    radius = 5000  # Search within 5 km
    query = 'restaurants'  # Type of business you are looking for

    print("Starting place search...")
    places = get_places(api_key, location, radius, query)

    if places and 'results' in places:
        print(f"Fetched places: {places}")
        results = places.get('results', [])
        print(f"Number of results: {len(results)}")

        for place in results:
            name = place.get('name')
            address = place.get('formatted_address')
            place_id = place.get('place_id')
            rating = place.get('rating', 0)  # Default rating to 0 if not available

            print(f"Checking place: {name} with rating: {rating}")

            # Filter for places with rating less than 4 and check if they have a website
            if rating < 4:
                details = get_place_details(api_key, place_id)
                if details:
                    website = details.get('website')
                    if not website:
                        print(f"Name: {name}\nAddress: {address}\nRating: {rating}\nPlace ID: {place_id}\n")
                        phone = details.get('formatted_phone_number')
                        print(f"Phone: {phone}\nWebsite: {website if website else 'No website'}\n")
                else:
                    print(f"Failed to get details for place ID: {place_id}")
    else:
        print("No places found or error fetching places")

if __name__ == "__main__":
    main()
