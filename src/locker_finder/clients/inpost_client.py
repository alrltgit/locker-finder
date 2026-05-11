import csv
import requests
import uuid
from io import StringIO
from src.locker_finder.utils.decorators import handle_runtime_error
from ..db.database import engine
from concurrent.futures import ThreadPoolExecutor, as_completed

class InPostClient:
    BASE_URL = "https://api-global-points.easypack24.net/v1/points?country=PL"

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()

    @handle_runtime_error
    def _fetch_page(self, page: int):
        """ Make the HTTP request and return parsed JSON """

        response = self.session.get(self.BASE_URL, params={"page": page}, timeout=10)
        response.raise_for_status()
        return response.json()

    def _fetch_pages_in_parallel(self, start: int, end: int, max_workers: int = 10):
        """ Fetch pages in parallel """

        results = []

        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            future_to_page = {
                executor.submit(self._fetch_page, page): page
                for page in range(start, end + 1)
            }

            for future in as_completed(future_to_page):
                data = future.result()
                results.append(data)

        return results

    def seed_lockers_to_db(self):

        buffer = StringIO()
        writer = csv.writer(buffer)

        pages_data = self._fetch_pages_in_parallel(1, 1360)

        for page_data in pages_data:
            items = page_data.get("items", [])

            for item in items:
                row = self.parse_data(item)
                writer.writerow(row)

        buffer.seek(0)

        connection = engine.raw_connection()
        cursor = connection.cursor()

        try:
            cursor.copy_expert(
                """
                COPY locker_finder.lockers (
                    id,
                    external_href,
                    name,
                    type,
                    status,
                    physical_type,
                    lat,
                    lon,
                    address_line1,
                    address_line2,
                    city,
                    province,
                    post_code,
                    open_hours,
                    is_24_7
                )
                FROM STDIN WITH CSV
                """,
                buffer
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def parse_data(item:dict) -> list:
        """ Map a raw API into a dict """
        location = item.get("location", {})
        address = item.get("address", {})
        address_details = item.get("address_details", {})

        return [
            str(uuid.uuid4()),
            item.get("href"),
            item.get("name"),
            item.get("type"),
            item.get("status"),
            item.get("physical_type"),
            location.get("latitude"),
            location.get("longitude"),
            address.get("line1"),
            address.get("line2"),
            address_details.get("city"),
            address_details.get("province"),
            address_details.get("post_code"),
            item.get("open_hours"),
            item.get("location_247", False)
        ]