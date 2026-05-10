import requests
import uuid
from ..utils.decorators import handle_runtime_error

class InPostClient:
    BASE_URL = "https://api-global-points.easypack24.net/v1/points"

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()

    @handle_runtime_error
    def _fetch(self, params: dict):
        """ Make the HTTP request and return parsed JSON """
        response = self.session.get(self.BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_lockers_data(self, latitude: float, longitude: float, radius: int = 5) -> list:
        """ Retrieve data from API """
        params = { "lat": latitude, "lon": longitude, "rad": radius}
        data = self._fetch(params)

        return self.organize_lockers(data)

    def organize_lockers(self, data) -> list:
        """ Convert raw API response into a list of lockers """
        lockers = []

        for item in data.get("items", []):
            lockers.append(self.parse_data(item))

        return lockers

    @staticmethod
    def parse_data(item:dict) -> dict:
        """ Map a raw API into a dict """
        location = item.get("location", {})
        address = item.get("address", {})
        address_details = item.get("address_details", {})
        locker_availability = item.get("locker_availability", {})

        return {
            "id": str(uuid.uuid4()),
            "external_href": item.get("href"),

            "name": item.get("name"),
            "type": item.get("type"),
            "status": item.get("status"),
            "physical_type": item.get("physical_type"),

            "lat": location.get("latitude"),
            "lon": location.get("longitude"),

            "address_line1": address.get("line1"),
            "address_line2": address.get("line2"),
            "city": address_details.get("city"),
            "province": address_details.get("province"),
            "post_code": address_details.get("post_code"),

            "open_hours": item.get("open_hours"),
            "is_24_7": item.get("location_247", False),
            "availability_status": locker_availability.get("longitude"),
        }