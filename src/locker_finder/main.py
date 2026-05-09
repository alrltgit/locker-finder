from .services.inpost_client import InPostClient
from .services.lockers_search import find_nearest_lockers

def main():
    client = InPostClient()

    user_lat = 52.2297
    user_lon = 21.0122

    lockers = client.get_lockers_data(user_lat, user_lon)
    nearest_lockers = find_nearest_lockers(lockers, user_lon, user_lat)

    print(f"Found: {len(nearest_lockers)} lockers\n")

    for l in nearest_lockers:
        print({
            "id": l["id"],
            "city": l["city"],
            "lat": l["lat"],
            "lon": l["lon"],
            "status": l["status"]
        })

if __name__ == '__main__':
    main()